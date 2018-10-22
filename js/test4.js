/**
 * 面向对象编程
 * 
 * 实例对象与new命令
 * this关键字
 * 对象的继承
 * Object对象的相关方法
 * 严格模式
 */

// 典型的面向对象编程语言（比如 C++ 和 Java），都有“类”（class）这个概念。所谓“类”就是对象的模板，对象就是“类”的实例。但是
// JavaScript 语言的对象体系，不是基于“类”的，而是基于构造函数（constructor）和原型链（prototype）

// new命令的作用，就是执行构造函数，返回一个实例对象
var Vehicle = function (p) {
    'use strict';//构造函数使用严格模式，必须跟new一起使用
    this.price = p;
};

var v = new Vehicle(500);
console.log("new 对象", v.price);
//忘记调用new,this变成一个全局对象。。
try {
    var v1 = Vehicle(600);
    console.log("new 对象", v1.price);
} catch (error) {
    console.log(error);
}

/**

new 命令的原理
使用new命令时，它后面的函数依次执行下面的步骤。

创建一个空对象，作为将要返回的对象实例。
将这个空对象的原型，指向构造函数的prototype属性。
将这个空对象赋值给函数内部的this关键字。
开始执行构造函数内部的代码。

也就是说，构造函数内部，this指的是一个新生成的空对象，所有针对this的操作，都会发生在这个空对象上。
构造函数之所以叫“构造函数”，就是说这个函数的目的，就是操作一个空对象（即this对象），将其“构造”为需要的样子。
如果构造函数内部有return语句，而且return后面跟着一个对象，new命令会返回return语句指定的对象；
否则，就会不管return语句，返回this对象

但是，如果return语句返回的是一个跟this无关的新对象，new命令会返回这个新对象，而不是this对象。
这一点需要特别引起注意

另一方面，如果对普通函数（内部没有this关键字的函数）使用new命令，则会返回一个空对象

 */
// new命令简化的内部流程，可以用下面的代码表示。
function _new(/* 构造函数 */ constructor, /* 构造函数参数 */ params) {
    // 将 arguments 对象转为数组
    var args = [].slice.call(arguments);
    // 取出构造函数
    var constructor = args.shift();
    // 创建一个空对象，继承构造函数的 prototype 属性
    var context = Object.create(constructor.prototype);
    // 执行构造函数
    var result = constructor.apply(context, args);
    // 如果返回结果是对象，就直接返回，否则返回 context 对象
    return (typeof result === 'object' && result != null) ? result : context;
}

// new.target
// 函数内部可以使用new.target属性。如果当前函数是new命令调用，new.target指向当前函数，否则为undefined。

function funcNetTarget() {
    // 使用这个属性，可以判断函数调用的时候，是否使用new命令。
    console.log("funcNetTarget", new.target === funcNetTarget);
}

funcNetTarget(); // false
new funcNetTarget(); // true

// Object.create() 创建实例对象
// 构造函数作为模板，可以生成实例对象。但是，有时拿不到构造函数，只能拿到一个现有的对象。
// 我们希望以这个现有的对象作为模板，生成新的实例对象，这时就可以使用Object.create()方法

// this
// 简单说，this就是属性或方法“当前”所在的对象。

/*
var obj = { foo:  5 };
上面的代码将一个对象赋值给变量obj。JavaScript 引擎会先在内存里面，生成一个对象{ foo: 5 }，然后把这个对象的内存地址赋值给变量obj。也就是说，变量obj是一个地址（reference）。后面如果要读取obj.foo，引擎先从obj拿到内存地址，然后再从该地址读出原始的对象，返回它的foo属性。
 
原始的对象以字典结构保存，每一个属性名都对应一个属性描述对象。举例来说，上面例子的foo属性，实际上是以下面的形式保存的。
 
{
  foo: {
    [[value]]: 5
    [[writable]]: true
    [[enumerable]]: true
    [[configurable]]: true
  }
}
注意，foo属性的值保存在属性描述对象的value属性里面
这样的结构是很清晰的，问题在于属性的值可能是一个函数。
var obj = { foo: function () {} };
这时，引擎会将函数单独保存在内存中，然后再将函数的地址赋值给foo属性的value属性。
{
  foo: {
    [[value]]: 函数的地址
    ...
  }
}
由于函数是一个单独的值，所以它可以在不同的环境（上下文）执行
 
this主要有以下几个使用场合
全局环境使用this，它指的就是顶层对象window (nodejs 没有这个)
*/
// console.log("this == window", this == window);

/*
var obj = {
    foo: function () {
        console.log(this);
    }
};
obj.foo() // obj
但是，下面这几种用法，都会改变this的指向。
情况一
(obj.foo = obj.foo)(); // window
// 情况二
(false || obj.foo)(); // window
// 情况三
(1, obj.foo)(); // window

如果this所在的方法不在对象的第一层，这时this只是指向当前一层的对象，而不会继承更上面的层。
var a = {
  p: 'Hello',
  b: {
    m: function() {
      console.log(this.p);
    }
  }
};
a.b.m() // undefined
上面代码中，a.b.m方法在a对象的第二层，该方法内部的this不是指向a，而是指向a.b，因为实际执行的是下面的代码
var b = {
  m: function() {
   console.log(this.p);
  }
};
var a = {
  p: 'Hello',
  b: b
};
(a.b).m() // 等同于 b.m()

避免多层 this
由于this的指向是不确定的，所以切勿在函数中包含多层的this
    使用一个变量固定this的值，然后内层函数调用这个变量，是非常常见的做法，请务必掌握。
避免数组处理方法中的 this
避免回调函数中的 this
*/
