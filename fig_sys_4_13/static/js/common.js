/**
 * Created by wxb on 18-2-1.
 */

function imgShow(outerdiv, innerdiv, bigimg, _this) {
			var src = _this.attr("src");
			$(bigimg).attr("src", src);

			/*获取当前点击图片的真实大小，并显示弹出层及大图*/
			$("<img/>").attr("src", src).load(function() {
				var windowW = $(window).width();
				var windowH = $(window).height();
				var realWidth = this.width;
				var realHeight = this.height;
				var imgWidth, imgHeight;
				var scale = 0.8;

				if(realWidth > windowW * scale) {
					imgWidth = windowW * scale;
					imgHeight = imgWidth / realWidth * realHeight;
				} else {
					imgWidth = realWidth;
					imgHeight = realHeight;
				}
				$(bigimg).css("width", imgWidth);

				var w = (windowW - imgWidth) / 2;
				var h = (windowH - imgHeight) / 2;
				if(h<0){
				    h = 60;
				};
				$(innerdiv).css({
					"top": h,
					"left": w,
					"bottom":10
				});
				$(outerdiv).fadeIn("fast");
			});

			$(outerdiv).click(function() {
				$(this).fadeOut("fast");
			});
		}