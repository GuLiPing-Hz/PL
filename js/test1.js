/**
 * 
 * 开始新的JavaScript学习
 */

/* 变量提升
 *  JavaScript 引擎的工作方式是，先解析代码，获取所有被声明的变量，然后再一行一行地运行。
 *  这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，这就叫做变量提升（hoisting）。
 */
console.log(a);//这里变量提升
var a = 1;
console.log(a);

/**
 * 变量提升
 * 上面的代码等价于:
 * var a;
 * console.log(a);
 * a = 1;
 * console.log(a);
 * 
 */

/**
 * 标识符
 * 
 * 第一个字符，可以是任意 Unicode 字母（包括英文字母和其他语言的字母），以及美元符号（$）和下划线（_）。
 * 第二个字符及后面的字符，除了 Unicode 字母、美元符号和下划线，还可以用数字0-9
 */

var 临时变量 = 1;
console.log("临时变量=" + 临时变量);

{
  var b = 2;//JavaScript 的区块不构成单独的作用域（scope）
}
console.warn(b);//这里也能访问a

switch (a) {//switch使用的是严格相等运算符 ===
  case true:
    console.log("发生类型转换");
    break;
  default:
    console.log("没有发生类型转换")
}

/**
 * js标签
 */
run: {
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      console.log("i = ");
      if (i === 1 && j === 1)
        break run;//break 搭配标签，跳出双层循环，continue也可以
      console.log(i + ";" + j);
    }
  }
}

/**
 * JavaScript 有三种方法，可以确定一个值到底是什么类型。
 * typeof运算符
 * instanceof运算符
 * Object.prototype.toString方法
 */
console.log("类型判断:");
console.log("typeof a=" + typeof a);
console.log("typeof ''=" + typeof "");
console.log("typeof true=" + typeof true);
var f = function () { }
console.log("typeof f=" + typeof f);
console.log("typeof undefined=" + typeof undefined);
/**
 * null的类型是object，这是由于历史原因造成的。
 * 1995年的 JavaScript 语言第一版，只设计了五种数据类型（对象、整数、浮点数、字符串和布尔值），
 * 没考虑null，只把它当作object的一种特殊值。后来null独立出来，作为一种单独的数据类型，
 * 为了兼容以前的代码，typeof null返回object就没法改变了。
 */
console.log("typeof null=" + typeof null);
console.log("typeof window=" + typeof window);

var arra = [];
console.log("typeof arra=" + typeof arra);
console.log("typeof {}=" + typeof {});

/*
判断一个值是否定义
// 错误的写法
if (v) {
  // ...
}
// ReferenceError: v is not defined

// 正确的写法
if (typeof v === "undefined") {
  // ...
}
*/

// instanceof 运算等级低
console.log("arra instanceof Array=" + (arra instanceof Array));
console.log(Object.prototype.toString(a));

console.log("undefined == null = " + (undefined == null));//这里不是严格相等
console.log("Number(null)=" + Number(null));//null依据c++的标准，自动转0
console.log("a + null = " + (a + null));

console.log("Number(undefined)=" + Number(undefined)) // NaN
console.log(5 + undefined) // NaN

/**
 * 转换规则是除了下面六个值被转为false，其他值都视为true
 * 
 * undefined
 * null
 * false
 * 0
 * NaN
 * ""或''（空字符串）
 */
console.log(!!"");

/**
 * JavaScript 内部，所有数字都是以64位浮点数形式储存，即使整数也是如此。
 * 所以，1与1.0是相同的，是同一个数
 */
console.log("1 === 1.0=" + (1 === 1.0));
console.log("0.1+0.2 === 0.3=" + (0.1 + 0.2 === 0.3));

/**
 * js 数值表示
 * 第1位：符号位，0表示正数，1表示负数
 * 第2位到第12位（共11位）：指数部分
 * 第13位到第64位（共52位）：小数部分（即有效数字）
 * 
 * 数值表达式： (-1)^符号位 * 1.xx...xx * 2^指数部分
 * 
 * IEEE 754 规定，如果指数部分的值在0到2047之间（不含两个端点），
 * 那么有效数字的第一位默认总是1，不保存在64位浮点数之中
 * 
 * 所以有效数字是 (正/负)1*1.(52位) * 2^(指数为1)
 * [-2^53 , 2^53] 有效数字表示范围，
 * 
 * 指数部分的表示范围是 -1023(开区间) ~0~ 1023 (2047各分一半) 
 * (正/负)* 0.(2^-52) * 2^-1023  小数部分最小取到 2^-52次幂
 * (正/负)* 1.99999 * 2^1023     小数部分最大取到 1.999999 < 2
 * (-2^1024,-2^-1075] and [2^-1075 , 2^1024) 
 */
console.log("数值精度测试");
console.log(Math.pow(2, 53));
console.log(Math.pow(2, 53) + 1);//超出有效数字范围，精度无法保证
console.log(Math.pow(-2, 53));
console.log(Math.pow(-2, 53) - 1);//超出有效数字范围，精度无法保证

console.log("数值范围测试");
console.log(Math.pow(2, 1023)); //
console.log(Math.pow(2, 1024)); // Infinity 正向溢出
console.log(Math.pow(2, -1075)); // 0
console.log(Math.pow(2, -1076)); // 0 负向溢出
console.log('Number.MAX_VALUE=' + Number.MAX_VALUE + "; + Number.MIN_VALUE=" + Number.MIN_VALUE);


