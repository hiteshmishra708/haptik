/*Animation1*/
$(document).ready(function(){
var left = 0;
var right = 0;
var items = $(".img_item");
animateImg(items,0,0,0);
});
var indexNum = 1;
var animateImg = function(items,left,height,indexNum){
if(items.length >= indexNum)
{
	if(indexNum == 0)
	{
		left = 150;
		height = 0;
	}
	if(indexNum == 1)
	{
		left = 150;
		height = 0;
		//right = 200;
	}
	if(indexNum == 2)
	{
		left = 150;
		height = 0;
	}
	if(indexNum == 3)
	{
		left = 150;
		height = 0;
	}
	if(indexNum == 4)
	{
		left = 0;
		height = 206;
	}
	var item = items.get(indexNum);
	if(indexNum == 0 || indexNum == 2)
	{
	$(item).animate(
				{
					left : left,
					top : height,
					//right : right,
					opacity: 1
				},800,function()
				{
//					left += 300;
					indexNum++;
/*					if(indexNum  % 6 == 0)
					{
						left = 0;
						height += 299;
					}
*/					console.log(items);
					animateImg(items,left,height,indexNum);
				});
		}
	if(indexNum == 1 || indexNum == 3)
	{
	$(item).animate(
				{
					right : left,
					top : height,
					//right : right,
					opacity: 1
				},800,function()
				{
//					left += 300;
					indexNum++;
/*					if(indexNum  % 6 == 0)
					{
						left = 0;
						height += 299;
					}
*/					console.log(items);
					animateImg(items,left,height,indexNum);
				});
		}
	if(indexNum == 4)
	{
	$(item).animate(
				{
					bottom : left,
					bottom : height,
					//right : right,
					opacity: 1
				},800,function()
				{
//					left += 300;
					indexNum++;
/*					if(indexNum  % 6 == 0)
					{
						left = 0;
						height += 299;
					}
*/					console.log(items);
					animateImg(items,left,height,indexNum);
				});
		}
	
	
	}
};
