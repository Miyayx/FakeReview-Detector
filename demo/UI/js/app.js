$(document).ready(function() {

	var jsondata = null
	var curdata = null
	var curpage = 1;
	var filtering = false
	var querystring = null

	var freshPage = function(data) {
		fakeNum = 0;
		data.forEach(function(d) {
			if (d.fake) fakeNum++;
		});
		$("#total-n").text(data.length);
		$("#fake-n").text(fakeNum);
		displayTable();
		curpage = 1;
	}

	var displayTable = function() {
		// Append Items to #contents here
		$('#contents').children().remove();
		displaydata = [];
		if (filtering) {
			jsondata.forEach(function(d) {
				if (d.fake) displaydata.push(d);
			});
		} else {
			displaydata = jsondata;
		}
		curdata = displaydata.slice((curpage - 1) * 8, curpage * 8);
		curdata.forEach(function(d) {
			var $elem = $('<tr><td>' + d.rid + '</td><td>' + d.review + '</td><td>' + d.reviewer + '</td><td>' + d.time + '</td></tr>');

			if (d.fake) $elem.addClass('error');
			$elem.appendTo('#contents');
		});
	}

	var buttonIntial = function() {

		var displayInput = function(input) {
			if (input.length > 0) {
				$("#input-show").css("display", "")
				$("#input-show span").text(input)
				querystring = input
			}
		}

		$("#one").click(function() {
			box = bootbox.prompt("输入评论", "取消", "确定", function(input) {
				displayInput(input)
			})
			box.find(":input:first").css({
				"width": 500,
				"height": 150
			})
		});

		$("#file").change(function() {
			displayInput($("#file").val().split('\\').pop());
		});

		$("#upload").click(function() {
			var s = document.getElementById("file");
			s.click();
			//displayInput(s.value)
		});

		$("#url").click(function() {
			box = bootbox.prompt("输入产品链接", "取消", "确定", function(input) {
				displayInput(input)
			})
			box.find(":input:first").css({
				"width": 500,
				"height": 150
			})
		});

		$("#filter").click(function() {
			if (jsondata) {
				if (filtering) {
					filtering = false;
					$("#filter").text("虚假评论");
					displayTable();
					curpage = 1;
				} else {
					filtering = true;
					$("#filter").text("所有评论");
					displayTable();
					curpage = 1;
				}
			}
		});

		$("#detect").click(function() {
			$.getJSON("/detect", {
				string: querystring
			},
			function(data) {
				jsondata = data;
				freshPage(data);
			});
		});
	}

	var displayPager = function() {

		$('#pages').children().remove();

		$pager = $(pagination({
			cur: curpage,
			max: 15
		}));

		$pager.find('.prev-page').click(function() {
			if ($(this).hasClass('disabled')) return false;
			curpage--;
			displayPager();
			return false;
		});
		$pager.find('.num-page').click(function() {
			if ($(this).hasClass('active')) return false;
			curpage = parseInt($(this).text());
			displayPager();
			return false;
		});
		$pager.find('.next-page').click(function() {
			if ($(this).hasClass('disabled')) return false;
			curpage++;
			displayPager();
			return false;
		});

		$pager.appendTo('#pages');

		$('#contents').children().remove();
		if (jsondata) {
			displayTable();
		} else {
			$.getJSON("review.json", function(data) {
				jsondata = data;
				freshPage(data);
			});

		}
	}
	displayPager();
	buttonIntial();
});

