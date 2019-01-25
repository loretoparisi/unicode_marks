const UNICODE_NSM = require('./data.json');

var countNonSpacingCharString = function(str) {
    var chars = str.split("");
    var count = 0;
    for (var i = 0,ilen = chars.length;i<ilen;i++) {
      if(UNICODE_NSM.indexOf(chars[i]) == -1) {
        count++;
       }
    }
    return count;
};

s="अब यहां से कहा जाएँ हम"
l=countNonSpacingCharString(s)
console.log( s, s.length, l)