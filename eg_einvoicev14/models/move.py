import json

import requests
from odoo import models, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Move(models.Model):
    _inherit = 'account.move'
    electronicInvoiceID = fields.Char(string='Electronic Invoice ID', readonly=False, copy=False)
    send_electronic_invoice = fields.Boolean(string="Send Electronic Invoice", copy=False)
    electronic_invoice_status = fields.Char(string="Electronic Invoice Status", required=False)

    def submit_invoice(self):
        if self.send_electronic_invoice == False:
            base_url = self.get_base_url()
            url = base_url + "/api/v1/documentsubmissions"
            access = self.login()
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",
                       'Authorization': "Bearer " + access}
            data = {
                'issuer': self.get_issuer(),
                'receiver': self.get_receiver()
            }
            data.update(self.get_other_data())
            data.update(self.get_invoice_lines())
            if self.company_id.invoiceVersion == '1.0':
                final_data = self.elec_sign()
            else:
                final_data = {'documents': [data]}
            final_data = json.dumps(final_data, ensure_ascii=False).encode('utf8')
            response = requests.request("POST", url, headers=headers, data=final_data, verify=False)
            _logger.warning(final_data)
            _logger.warning(response.json())

            if response.status_code == 202:
                if response.json():
                    if response.json().get('acceptedDocuments'):
                        if response.json().get('acceptedDocuments')[0].get('uuid'):
                            self.electronicInvoiceID = response.json().get('acceptedDocuments')[0].get('uuid')
                            self.send_electronic_invoice = True
            else:
                response = response.json()
                if response:
                    if response.get('error') and isinstance(response.get('error'), dict):
                        if response.get('error').get('details'):
                            if response.get('error').get('details')[0].get('message'):
                                raise ValidationError(response.get('error').get('details')[0].get('message'))
                        if response.get('error').get('message'):
                            if response.get('error').get('message'):
                                raise ValidationError(response.get('error').get('message'))
                    else:
                        raise ValidationError(response.get('error'))

    def print_invoice(self):
        base_url = self.get_base_url()
        url = base_url + "/api/v1/documents/" + str(self.electronicInvoiceID) + "/details"
        access = self.login()
        headers = {'Content-Type': "application/json", 'cache-control': "no-cache", 'Authorization': "Bearer " + access}
        response = requests.request("GET", url, headers=headers, verify=False)
        response = response.json()['publicUrl']
        try:
            return {'name': self.electronicInvoiceID,
                    'res_model': 'ir.actions.act_url',
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': response
                    }
        except:
            pass

    def get_base_url(self):
        configType = self.company_id.configType
        if configType == 'UAT':
            return "https://api.preprod.invoicing.eta.gov.eg"
        if configType == 'PRD':
            return "https://api.invoicing.eta.gov.eg"
        if configType == 'SIT':
            return "https://api.sit.invoicing.eta.gov.eg"

    def get_idSrv_url(self):
        configType = self.company_id.configType
        if configType == 'UAT':
            return "https://id.preprod.eta.gov.eg"
        if configType == 'PRD':
            return "https://id.eta.gov.eg"
        if configType == 'SIT':
            return "https://id.sit.eta.gov.eg"

    def get_clientId_Secret(self):
        return self.company_id.clientId, self.company_id.clientSecret

    def login(self):
        idSrv = self.get_idSrv_url()
        url = idSrv + "/connect/token"
        clientId, clientSecret = self.get_clientId_Secret()
        headers = {'content-type': "application/x-www-form-urlencoded", 'cache-control': "no-cache"}
        payload = {
            'grant_type': 'client_credentials',
            'client_id': clientId,
            'client_secret': clientSecret,
            'scope': 'InvoicingAPI',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json().get('error'):
            raise ValidationError(_(response.json().get('error')))
        _logger.warning(response.text)

        try:
            return response.json()['access_token']
        except:
            return False

    def cancel_reject(self, status, reason):
        base_url = self.get_base_url()
        url = base_url + "/api/v1.0/documents/state/" + str(self.electronicInvoiceID) + "/state"
        access = self.login()
        headers = {'Content-Type': "application/json", 'cache-control': "no-cache", 'Authorization': "Bearer " + access}
        payload = {
            'status': status,
            'reason': reason
        }
        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=headers, data=payload.encode('utf-8'), verify=False)
        if response.status_code == 200:
            self.electronic_invoice_status = status
        else:
            response = response.json()
            print(">>", response)
            if response.get('error'):
                if response.get('error').get('details'):
                    if response.get('error').get('details')[0].get('message'):
                        raise ValidationError(response.get('error').get('details')[0].get('message'))
                if response.get('error').get('message'):
                    if response.get('error').get('message'):
                        print("F>>>>>>>>>", response.get('error').get('message'))
                        raise ValidationError(response.get('error').get('message'))

    def get_issuer(self):
        data = {
            'address': {
                'branchID': self.company_id.branchID or "branchID",
                'country': "EG",
                'governate': self.company_id.governateE or "governate",
                'regionCity': self.company_id.regionCity or "regionCity",
                'street': self.company_id.street or "street",
                'buildingNumber': self.company_id.buildingNumber or "buildingNumber",
                'postalCode': self.company_id.zip or "postalCode",
                'floor': self.company_id.floor or "floor",
                'room': self.company_id.room or "room",
                'landmark': self.company_id.landmark or "landmark",
                'additionalInformation': self.company_id.additionalInformation or "additionalInformation"

            },
            'type': self.company_id.person_type,
            'id': self.company_id.reg_no,
            'name': self.company_id.name,
        }
        return data

    def get_receiver(self):
        data = {
            'address': {
                'country': "EG",
                'governate': self.partner_shipping_id.governateE or "governate",
                'regionCity': self.partner_shipping_id.regionCity or "regionCity",
                'street': self.partner_shipping_id.street or "street",
                'buildingNumber': self.partner_shipping_id.buildingNumber or "buildingNumber",
                'postalCode': self.partner_shipping_id.zip or "postalCode",
                'floor': self.partner_shipping_id.floor or "floor",
                'room': self.partner_shipping_id.room or "room",
                'landmark': self.partner_shipping_id.landmark or "landmark",
                'additionalInformation': self.partner_shipping_id.additionalInformation or "additionalInformation"

            },
            'type': self.partner_shipping_id.person_type,
            'id': self.partner_shipping_id.vat,
            'name': self.partner_id.name,
        }
        return data

    def get_other_data(self):
        invoiceVersion = self.company_id.invoiceVersion
        if self.move_type == 'out_refund':
            doc_type = 'C'
        elif self.move_type == 'in_refund':
            doc_type = 'D'
        else:
            doc_type = 'I'
        data = {
            'documentType': doc_type,
            'documentTypeVersion': invoiceVersion,
            'dateTimeIssued': str(self.invoice_date) + "T00:00:00Z",
            'taxpayerActivityCode': self.company_id.activity_code,
            'internalID': self.name,

        }
        print(data)
        _logger.warning(data)
        return data

    def elec_sign(self):
        data = {
            'issuer': self.get_issuer(),
            'receiver': self.get_receiver()
        }
        data.update(self.get_other_data())
        data.update(self.get_invoice_lines())
        sign_url = self.company_id.sign_url

        final_data = json.dumps(data, ensure_ascii=False).encode('utf8')
        headers = {'Content-Type': "application/json"}
        response = requests.request("POST", sign_url + '/SigningService', headers=headers,
                                    data=final_data, )
        return response.json()

    def get_invoice_lines(self):
        taxTotals = self.amount_tax if self.amount_tax else 0
        lines = []
        total_discount = 0
        total_salesTotalAmount = 0
        # include = False
        for line in self.invoice_line_ids:
            price_unit_wo_discount = line.price_unit * (1 - (line.discount / 100.0))
            taxes_res = line.tax_ids._origin.compute_all(price_unit_wo_discount,
                                                         quantity=line.quantity, currency=line.currency_id,
                                                         product=line.product_id,
                                                         partner=line.partner_id)
            taxableItems = line._get_taxableItems(taxes_res['taxes'])
            description = line.product_id.name if line.product_id.name else "description"
            if line.lot_id:
                description += "-" + line.lot_id.name
            itemCode = line.product_id.item_code if line.product_id.item_code else line.product_id.id
            itemType = line.product_id.item_type if line.product_id.item_type else "EGS"
            unitType = line.unit_type_id.code if line.unit_type_id else "EA"
            # taxTypesCode = line.tax_type_id.code if line.tax_type_id else "T1"
            # subTaxTypesCode = line.sub_tax_type_id.code if line.sub_tax_type_id else "V008"
            quantity = line.quantity if line.quantity else 1
            amountEGP = line.price_unit if line.price_unit else 1
            salesTotal = str(line.price_subtotal) if line.price_subtotal else 1
            rate = line.discount if line.discount else 0
            discount_amount = (rate / 100) * amountEGP * quantity
            total_discount += discount_amount
            tax_amount = (line.price_total - line.price_subtotal)
            # if line.tax_ids:
            #     include = line.tax_ids[0].price_include
            #     if include:
            #         amountEGP = (line.price_unit - tax_amount) if line.price_unit else 1
            if taxes_res:
                for tax in taxes_res['taxes']:
                    if tax['price_include']:
                        amountEGP = (line.price_unit - tax['amount']) if line.price_unit else 1

            total_line = line.price_subtotal + tax_amount
            tax_amount = round(tax_amount, 3) if line.tax_ids else 0
            salesTotalAmount = amountEGP * quantity
            total_salesTotalAmount += salesTotalAmount
            tax_rate = 14 if line.tax_ids else 0
            calcu = amountEGP * quantity - discount_amount
            # ----------quantity-----------
            quantity = '%.5f' % quantity
            # ----------total_line-----------
            if type(total_line) is float:
                total_line = '%.5f' % total_line
            else:
                total_line = str(total_line)
            # ----------calcu-----------
            if type(calcu) is float:
                calcu = '%.5f' % calcu
            else:
                calcu = str(calcu)
            # ----------amountEGP-----------
            if type(amountEGP) is float:
                amountEGP = '%.5f' % amountEGP
            else:
                amountEGP = str(amountEGP)
            # ----------rate-----------
            if type(rate) is float:
                rate = '%.5f' % rate
            else:
                rate = str(rate)
            # ----------discount_amount-----------
            if type(discount_amount) is float:
                discount_amount = '%.5f' % discount_amount
            else:
                discount_amount = str(discount_amount)
            # ----------tax_amount-----------
            if type(tax_amount) is float:
                tax_amount = '%.5f' % tax_amount
            else:
                tax_amount = str(tax_amount)
            # ---------salesTotalAmount------------
            if type(salesTotalAmount) is float:
                salesTotalAmount = '%.5f' % salesTotalAmount
            else:
                salesTotalAmount = str(salesTotalAmount)
            # ---------tax_rate------------
            if type(tax_rate) is float:
                tax_rate = '%.5f' % tax_rate
            else:
                tax_rate = str(tax_rate)
            # ---------------------
            lines.append(
                {
                    'description': description,
                    'itemType': itemType,
                    'itemCode': itemCode,
                    'internalCode': itemCode,
                    'unitType': unitType,
                    'quantity': float(quantity),
                    'unitValue': {
                        'currencySold': 'EGP',
                        'amountSold': 0,
                        'currencyExchangeRate': 0,
                        'amountEGP': float(amountEGP)},
                    'salesTotal': float(salesTotal),
                    'valueDifference': 0,
                    'totalTaxableFees': 0,
                    'discount': {
                        'rate': float(rate),
                        'amount': float(discount_amount),
                    },
                    'netTotal': float(calcu),
                    'itemsDiscount': 0,
                    'taxableItems': taxableItems,
                    'total': float(total_line)
                },

            )
        totalSalesAmount = total_salesTotalAmount  # self.amount_untaxed if self.amount_untaxed else 0
        totalDiscountAmount = total_discount if total_discount else 0
        netAmount = totalSalesAmount - totalDiscountAmount
        totalAmount = round(netAmount + self.amount_tax, 3)
        netAmount = netAmount
        totalSalesAmount = totalSalesAmount

        # ---------totalSalesAmount------------
        if type(totalSalesAmount) is float:
            totalSalesAmount = '%.5f' % totalSalesAmount
        else:
            totalSalesAmount = str(totalSalesAmount)
        # ---------totalDiscountAmount------------
        if type(totalDiscountAmount) is float:
            totalDiscountAmount = '%.5f' % totalDiscountAmount
        else:
            totalDiscountAmount = str(totalDiscountAmount)
        # ---------netAmount------------
        if type(netAmount) is float:
            netAmount = '%.5f' % netAmount
        else:
            netAmount = str(netAmount)

        print(type(netAmount))
        # ---------totalAmount------------
        if type(totalAmount) is float:
            totalAmount = '%.5f' % totalAmount
        else:
            totalAmount = str(totalAmount)

        data = {
            'invoiceLines': lines,
            'totalSalesAmount': float(totalSalesAmount),
            'totalDiscountAmount': float(totalDiscountAmount),
            'netAmount': float(netAmount),
            'totalAmount': float(totalAmount),
            'extraDiscountAmount': 0,
            'totalItemsDiscountAmount': 0,
        }
        return data
