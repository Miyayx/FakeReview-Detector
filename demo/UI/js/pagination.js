function pagination(locals, attrs, escape, rethrow, merge) {
attrs = attrs || jade.attrs; escape = escape || jade.escape; rethrow = rethrow || jade.rethrow; merge = merge || jade.merge;
var buf = [];
with (locals || {}) {
var interp;
buf.push('<div class="pagination pagination-large"><ul>');
 if(cur == 1) {
buf.push('<li class="prev-page disabled"><a href="#">«</a></li>');
 }else{
buf.push('<li class="prev-page"><a href="#">«</a></li>');
 }
 var lower, upper;
 if(cur < 3) {
   lower = 1;
 }else{
   lower = cur - 2;
 }
 upper = lower + 4;
 if(upper > max) {
   upper = max;
 }
 lower = upper - 4;
 if(lower < 1) {
   lower = 1;
 }
 for(var i = lower; i <= upper; i++) {
   if(i == cur) {
buf.push('<li class="num-page active"><a');
buf.push(attrs({ 'href':('#'), 'data-pagenum':('' + (i) + '') }, {"href":true,"data-pagenum":true}));
buf.push('>' + escape((interp = i) == null ? '' : interp) + '</a></li>');
   }else{
buf.push('<li class="num-page"><a');
buf.push(attrs({ 'href':('#'), 'data-pagenum':('' + (i) + '') }, {"href":true,"data-pagenum":true}));
buf.push('>' + escape((interp = i) == null ? '' : interp) + '</a></li>');
   }
 }
 if(cur == max) {
buf.push('<li class="next-page disabled"><a href="#">»</a></li>');
 }else{
buf.push('<li class="next-page"><a href="#">»</a></li>');
}
buf.push('</ul></div>');
}
return buf.join("");
}
