/**
 * 
 * 开始新的JavaScript学习
 * 
 * 本篇内容：
 * Object对象
 * 属性描述对象
 * Array对象
 * 包装对象
 * Boolean对象
 * Number对象
 * String对象
 * Math对象
 * Date对象
 * RegExp对象
 * JSON对象
 * 
 */

/**
 * Object对象
 * Object对象本身的方法-静态方法
 *     所谓”本身的方法“就是直接定义在Object对象的方法
 * 
 * Object的实例方法
 *     所谓实例方法就是定义在Object原型对象Object.prototype上的方法。它可以被Object实例直接使用。
 */

var obj1 = Object();
// 等同于
var obj2 = Object(undefined);//不建议这样写，累赘
var obj3 = Object(null);//不建议这样写，累赘
console.log("obj2 instanceof Object:", obj2 instanceof Object);

/**
 * Object函数的参数是各种原始类型的值，转换成对象就是原始类型值对应的包装对象。
 * 
    var obj = Object(1);
    obj instanceof Object // true
    obj instanceof Number // true

    var obj = Object('foo');
    obj instanceof Object // true
    obj instanceof String // true

    var obj = Object(true);
    obj instanceof Object // true
    obj instanceof Boolean // true

    如果Object方法的参数是一个对象，它总是返回该对象，即不用转换
 */
//自定义判断是否对象的方法
function isObject(value) {
    return value === Object(value);
}

/**
 * 注意，通过var obj = new Object()的写法生成新对象，与字面量的写法var obj = {}是等价的。
 * 或者说，后者只是前者的一种简便写法
 * 
 * 虽然用法相似,Object(value)与new Object(value)两者的语义是不同的，
 * Object(value)表示将value转成一个对象，new Object(value)则表示新生成一个对象，它的值是value。
 */

/**
 * Object.keys方法和Object.getOwnPropertyNames方法都用来遍历对象的属性
 * 
 * 对于一般的对象来说，Object.keys()和Object.getOwnPropertyNames()返回的结果是一样的
 * Object.keys方法只返回可枚举的属性，
 * Object.getOwnPropertyNames方法还返回不可枚举的属性名。
 * 
 * 一般情况下，几乎总是使用Object.keys方法，遍历数组的属性
 */
var arra = [1, 2, 3];
console.log("获取对象属性", Object.keys(arra), Object.getOwnPropertyNames(arra));
console.log("\n");
/**
 * 其他对象静态方法
 * 
    （1）对象属性模型的相关方法
        Object.getOwnPropertyDescriptor()：获取某个属性的描述对象。
        Object.defineProperty()：通过描述对象，定义某个属性。
        Object.defineProperties()：通过描述对象，定义多个属性。
    （2）控制对象状态的方法
        Object.preventExtensions()：防止对象扩展。
        Object.isExtensible()：判断对象是否可扩展。
        Object.seal()：禁止对象配置。
        Object.isSealed()：判断一个对象是否可配置。
        Object.freeze()：冻结一个对象。
        Object.isFrozen()：判断一个对象是否被冻结。
    （3）原型链相关方法
        Object.create()：该方法可以指定原型对象和属性，返回一个新的对象。
        Object.getPrototypeOf()：获取对象的Prototype对象。
 */

/**
 * 对象的实例方法
   
   Object实例对象的方法，主要有以下六个。
       Object.prototype.valueOf()：返回当前对象对应的值。
       Object.prototype.toString()：返回当前对象对应的字符串形式。
       Object.prototype.toLocaleString()：返回当前对象对应的本地字符串形式。
       Object.prototype.hasOwnProperty()：判断某个属性是否为当前对象自身的属性，还是继承自原型对象的属性。
       Object.prototype.isPrototypeOf()：判断当前对象是否为另一个对象的原型。
       Object.prototype.propertyIsEnumerable()：判断某个属性是否可枚举。
            实例对象的propertyIsEnumerable()方法返回一个布尔值，用来判断某个属性是否可遍历。
            注意，这个方法只能用于判断对象自身的属性，对于继承的属性一律返回false。
*/

//valueOf方法的作用是返回一个对象的“值”，默认情况下返回对象本身。数据类型转换的时候会用到它

// toString方法是返回一个对象的字符串形式
// 数组、字符串、函数、Date 对象都分别部署了自定义的toString方法，覆盖了Object.prototype.toString方法
// 我们也可以自定定义toString方法覆盖Object.prototype.toString方法
var my = {
    toString: function () {
        return "Glp";
    }
};
// var my = new Object();
// my.toString = function () {
//     return "Glp";
// };
console.log("" + my, Object.prototype.toString.call(my));

//Object.prototype.toString可以实现比type更精确的类型判断
function myType(val) {
    var str = Object.prototype.toString.call(val);
    var strs = str.match(/\[object (.*)\]/);
    console.log(str, strs);

    var ret = strs[1].toLowerCase();
    console.log(ret);

    return ret;
}

myType({}); // "object"
myType([]); // "array"
myType(5); // "number"
myType(null); // "null"
myType(); // "undefined"
myType(/abcd/); // "regex"
myType(new Date()); // "date"

['Null',
    'Undefined',
    'Object',
    'Array',
    'String',
    'Number',
    'Boolean',
    'Function',
    'RegExp'
].forEach(function (t, i) {
    myType['is' + t] = function (o) {
        return myType(o) === t.toLowerCase();
    };
});

console.log("myType.isNull(null)=", myType.isNull(null));

/**
 * 属性描述对象
 * 
 */
//下面是属性描述对象的一个例子
var proto = {
    value: 123,//value是该属性的属性值，默认为undefined
    writable: false,//writable是一个布尔值，表示属性值（value）是否可改变（即是否可写），默认为true。

    //enumerable是一个布尔值，表示该属性是否可遍历，默认为true
    //如果设为false，会使得某些操作（比如for...in循环、Object.keys()）跳过该属性
    enumerable: true,

    //configurable是一个布尔值，表示可配置性，默认为true。
    //如果设为false，将阻止某些操作改写该属性，比如无法删除该属性，
    //也不得改变该属性的属性描述对象（value属性除外）。
    //也就是说，configurable属性控制了属性描述对象的可写性
    configurable: false,
    get: undefined,//get是一个函数，表示该属性的取值函数（getter），默认为undefined
    set: undefined//set是一个函数，表示该属性的存值函数（setter），默认为undefined
}

var obj = { p: 'a' };
console.log("获取属性描述", Object.getOwnPropertyDescriptor(obj, 'p'));
//注意，Object.getOwnPropertyDescriptor()方法只能用于对象自身的属性，不能用于继承的属性

// Object.getOwnPropertyNames方法返回一个数组，成员是参数对象自身的全部属性的属性名，不管该属性是否可遍历
var obj1 = Object.defineProperties({}, {
    p1: { value: 1, enumerable: true },
    p2: { value: 2, enumerable: false }
});
console.log("Object.getOwnPropertyNames", Object.getOwnPropertyNames(obj1), Object.keys(obj1));

var obj2 = Object.defineProperty({}, "p", {
    value: 123,
    writable: false,
    enumerable: true,
    configurable: false,

    //注意，一旦定义了取值函数get（或存值函数set），
    //就不能将writable属性设为true，或者同时定义value属性，否则会报错
    // get: undefined,
    // set: undefined

    /*
    var obj = {};
    Object.defineProperty(obj, 'p', {
    value: 123,
    get: function() { return 456; }
    });
    // TypeError: Invalid property.
    // A property cannot both have accessors and be writable or have a value

    Object.defineProperty(obj, 'p', {
    writable: true,
    get: function() { return 456; }
    });
    // TypeError: Invalid property descriptor.
    // Cannot both specify accessors and a value or writable attribute
    */
});
console.log("Object.defineProperty 不可写1", obj2.p);
obj2.p = 200;//这里因为定义属性的时候writable属性是false，所以不能写入成功
console.log("Object.defineProperty 不可写2", obj2.p);

/*
元属性
    value属性是目标属性的值

    writable属性是一个布尔值，决定了目标属性的值（value）是否可以被改变
    如果是false，在'use strict'严格模式会报错，普通只是默默的写入失败

    enumerable（可遍历性）返回一个布尔值，表示目标属性是否可遍历
    具体来说，如果一个属性的enumerable为false，下面三个操作不会取到该属性。
        for..in循环
        Object.keys方法
        JSON.stringify方法

        注意，for...in循环包括继承的属性，Object.keys方法不包括继承的属性

        如果需要获取对象自身的所有属性，不管是否可遍历，可以使用Object.getOwnPropertyNames方法。
        JSON.stringify方法会排除enumerable为false的属性，有时可以利用这一点。
            如果对象的 JSON 格式输出要排除某些属性，就可以把这些属性的enumerable设为false。

    configurable(可配置性）返回一个布尔值，决定了是否可以修改属性描述对象
        obj.p的configurable为false。然后，改动value、writable、enumerable、configurable，结果都报错。
        注意，writable只有在false改为true会报错，true改为false是允许的

        至于value，只要writable和configurable有一个为true，就允许改动
        另外，configurable为false时，直接目标属性赋值，不报错，但不会成功;如果是严格模式，还会报错。
        
        可配置性决定了目标属性是否可以被删除（delete）

    存取器
        除了直接定义以外，属性还可以用存取器（accessor）定义。其中，存值函数称为setter，
        使用属性描述对象的set属性；取值函数称为getter，使用属性描述对象的get属性。
*/
var obj3 = Object.defineProperty({}, 'p', {
    get: function () {
        return 'getter';
    },
    set: function (value) {
        console.log('setter: ' + value);
    }
});

console.log(obj3.p); // "getter"
obj3.p = 123 // "setter: 123"

// JavaScript 还提供了存取器的另一种写法。
var obj4 = {//这个写法跟obj3是等价的
    get p() {
        return 'getter';
    },
    set p(value) {
        console.log('setter: ' + value);
    }
};
//注意，取值函数get不能接受参数，存值函数set只能接受一个参数（即属性的值）
console.log("\n");

/**
 * 对象的拷贝
 */
var extend = function (to, from) {
    for (var property in from) {
        to[property] = from[property];
    }
    return to;
};
var copy1 = extend({}, {
    a: 1
});
var src2 = {
    get a() { return 1 }
};
console.log("对象的拷贝1:", src2.a, copy1);
var copy2 = extend({}, src2);
src2.a = 10;
copy2.a = 10;
console.log("对象的拷贝2:", src2.a, copy2.a, copy2);//拷贝后的对象可以对a值进行修改，

//为了解决这个问题，我们可以通过Object.defineProperty方法来拷贝属性
var extend2 = function (to, from) {
    for (var property in from) {
        if (!from.hasOwnProperty(property)) continue;

        //这里把from的属性拷贝到to
        Object.defineProperty(
            to,
            property,
            Object.getOwnPropertyDescriptor(from, property)
        );
    }

    return to;
};
var copy3 = extend2({}, src2);
copy3.a = 20;
console.log("对象的拷贝3:", src2.a, copy3.a, copy3);
