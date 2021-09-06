###### 喵

比赛的时候觉得这道题还挺好玩的。

最开始是想直接恢复`/flag`，思路是对了，但是信息不够，一直找不到什么好办法。

赛后有人在Discord上给出了提示：

> Instead of leaking /flag, you can try to leak main.js on the server. Although you can only get the amount of the unique character in a range, it's not a big deal, though. You can recover the original code since the file follows the syntax of JavaScript, it's not as difficult as recovering the content of the flag (because there are some random characters being added to the flag). After recovering main.js, you'll find it trivial.

原来`/main.js`也是有用的…

###### 思路

记区间$[i,j]$的entropy为$f(i,j)$。考虑一种情况，区间的首尾是相同的字符，且除去首尾以外的中间部分不包含这一字符。这种情况有什么性质呢？记中间部分的entropy为$x$，即$x = f(i+1,j-1)$。因为中间部分不包含首尾的字符，所以当首尾的字符分别纳入计算时，entropy都是$x+1$。又因为首尾的字符相同，当首尾的字符共同纳入计算时，entropy依旧是$x+1$。至此得出了一些必要条件：
$$
\begin{align}
f(i+1,j-1) &= x\\
f(i,j-1) &= x+1\\
f(i+1,j) &= x+1\\
f(i,j) &= x+1\\
\end{align}
$$
容易验证这其实是充要条件。通过这个规律我们可以确定整个文件中同一字符的所有位置（如果这个字符至少出现2次）。

最后通过js语言的一些特征和题目中给出的端口信息可以基本恢复出整个文件。比如：确定`\n` -> 确定`import` -> ...

