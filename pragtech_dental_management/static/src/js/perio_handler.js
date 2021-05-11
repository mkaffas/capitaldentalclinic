window.onload = function() {
};

$(document).ready(function() {
	function getCursorPosition(tooth, position) {
		var x,
		    y,
		    canvas_id;
		if (position == 'bleeding_1') {
			x = 15;
			y = 30;
			canvas_id = 'c_front_' + tooth;
			console.log('selectedddddddddd', x, y, canvas_id, tooth);
		} else if (position == 'bleeding_2') {
			x = 30;
			y = 30;
			canvas_id = 'c_front_' + tooth;
		} else if (position == 'bleeding_3') {
			x = 45;
			y = 30;
			canvas_id = 'c_front_' + tooth;
		} else if (position == 'bleeding_4') {
			x = 15;
			y = 30;
			canvas_id = 'c_back_' + tooth;
		} else if (position == 'bleeding_5') {
			x = 30;
			y = 30;
			canvas_id = 'c_back_' + tooth;
		} else if (position == 'bleeding_6') {
			x = 45;
			y = 30;
			canvas_id = 'c_back_' + tooth;
		}
		var canvas = document.getElementById(canvas_id);
		var ctx = canvas.getContext("2d");
		console.log(canvas);
		console.log(ctx);
		if (canvas_id) {
			ctx.beginPath();
			ctx.arc(x, y, 3, 0, Math.PI * 2, true);
			ctx.closePath();
			ctx.fill();
		}

	}

	function draw_canvas(img_obj, canvas_obj) {
		console.log("************* draw canvas ******* ", img_obj, canvas_obj);
		var ctx_canvas = canvas_obj.getContext("2d");
		console.log('this old oneeeeeeee', ctx_canvas);
		$(img_obj).on('load', function() {
			console.log('check', img_obj, canvas_obj);
			ctx_canvas.drawImage(img_obj, 0, 0, 60, 60);
			ctx_canvas.fillStyle = 'red';
		});
	}

	// var i = 1;
	//
	// for (var i = 1; i <= 32; i++) {
	// alert('check');
	// console.log('hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',document.getElementById('save_here'),$('#save_here').val());
	// var actual_id = 'front_' + i;
	// var canvas_id = 'c_' + actual_id;
	// var canvas = document.getElementById(canvas_id);
	// var img = document.getElementById(actual_id);
	// draw_canvas(img, canvas);
	// }
	//
	// for (var i = 1; i <= 32; i++) {
	// var actual_id = 'back_' + i;
	// var canvas_id = 'c_' + actual_id;
	// var canvas = document.getElementById(canvas_id);
	// var img = document.getElementById(actual_id);
	// draw_canvas(img, canvas);
	// }
	//
	// for (var i = 1; i <= 6; i++) {
	// $('#bleeding_' + i).click(function() {
	// console.log('check if true', ($('#' + this.id).is(":checked")));
	// console.log('clickedddd', this.id);
	// if (($('#' + this.id).is(":checked"))) {
	// var tooth = $('#selected_tooth').val();
	// if (!tooth) {
	// alert('No tooth selected');
	// ($('#' + this.id).attr("checked", false));
	// return;
	// }
	// canvas_id = 'c_front_' + tooth;
	// var canvas = document.getElementById(canvas_id);
	// var ctx = canvas.getContext("2d");
	// var img = document.getElementById(actual_id);
	// ctx.fillStyle = 'red';
	// getCursorPosition(tooth, this.id);
	// }
	// });
	// }
});

