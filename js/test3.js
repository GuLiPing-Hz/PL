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
obj3.p = 123; // "setter: 123"

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

/**
 * 控制对象状态
 * 有时需要冻结对象的读写状态，防止对象被改变。JavaScript 提供了三种冻结方法，
 * 最弱的一种是Object.preventExtensions，其次是Object.seal，最强的是Object.freeze
 *      Object.preventExtensions方法可以使得一个对象无法再添加新的属性
 *      Object.isExtensible方法用于检查一个对象是否使用了Object.preventExtensions方法。
 *          也就是说，检查是否可以为一个对象添加属性
 * 
 *      Object.seal方法使得一个对象既无法添加新属性，也无法删除旧属性
 *      Object.isSealed方法用于检查一个对象是否使用了Object.seal方法
 * 
 *      Object.freeze方法可以使得一个对象无法添加新属性、无法删除旧属性、也无法改变属性的值，使得这个对象实际上变成了常量
 *      Object.isFrozen方法用于检查一个对象是否使用了Object.freeze方法
 */

/**
 * 局限性
 * 上面的三个方法锁定对象的可写性有一个漏洞：可以通过改变原型对象，来为对象增加属性
 */
var obj = new Object();
Object.preventExtensions(obj);

var proto = Object.getPrototypeOf(obj);
proto.t = 'hello';
console.log("改变原型对象，来为对象增加属性", obj.t);
//一种解决方案是，把obj的原型也冻结住

/**
 * 另外一个局限是，如果属性值是对象，上面这些方法只能冻结属性指向的对象，而不能冻结对象本身的内容。
 */
var obj1 = {
    foo: 1,
    bar: ['a', 'b']
};
Object.freeze(obj1);

obj1.bar.push('c');
// obj1.bar // ["a", "b", "c"]
console.log("属性值是对象,无法确保内容不变", obj.t);
//综上，阻止扩张，密封，冰冻，并不能很好的使用。

/**
 * Array对象
 * Array是 JavaScript 的原生对象，同时也是一个构造函数，可以用它生成新的数组
 * 
 * var arr = new Array(2);
 * // 等同于
 * var arr = Array(2);
 */
var arra = new Array(2);
console.log("arra = ", arra, arra.length);

/*
    Array构造函数行为多变
        // 无参数时，返回一个空数组
        new Array() // []

        // 单个正整数参数，表示返回的新数组的长度
        new Array(1) // [ empty ]
        new Array(2) // [ empty x 2 ]

        // 非正整数的数值作为参数，会报错
        new Array(3.2) // RangeError: Invalid array length
        new Array(-3) // RangeError: Invalid array length

        // 单个非数值（比如字符串、布尔值、对象等）作为参数，
        // 则该参数是返回的新数组的成员
        new Array('abc') // ['abc']
        new Array([1]) // [Array[1]]

        // 多参数时，所有参数都是返回的新数组的成员
        new Array(1, 2) // [1, 2]
        new Array('a', 'b', 'c') // ['a', 'b', 'c']

    可以看到，Array作为构造函数，行为很不一致。因此，不建议使用它生成新数组，直接使用数组字面量是更好的做法
        // bad
        var arr = new Array(1, 2);
        // good
        var arr = [1, 2];

    注意，如果参数是一个正整数，返回数组的成员都是空位。虽然读取的时候返回undefined，
    但实际上该位置没有任何值。虽然可以取到length属性，但是取不到键名
*/
var a = new Array(3);
var b = [undefined, undefined, undefined];
console.log("Array 和 数组字面量创建数组的比较", a.length, b.length, a[0], b[0], 0 in a, 0 in b);

/**
 * 数组静态方法
 * 
 * Array.isArray方法返回一个布尔值，表示参数是否为数组。它可以弥补typeof运算符的不足
 */
console.log(typeof a, Array.isArray(a));

/**
 * 数组实例方法
 * valueOf()，toString()
 * valueOf方法是一个所有对象都拥有的方法，表示对该对象求值。不同对象的valueOf方法不尽一致，数组的valueOf方法返回数组本身
 * toString方法也是对象的通用方法，数组的toString方法返回数组的字符串形式
 */
console.log("valueOf,toString", a.valueOf(), a.toString());

// push方法用于在数组的末端添加一个或多个元素，并返回添加新元素后的数组长度。注意，该方法会改变原数组
// pop方法用于删除数组的最后一个元素，并返回该元素。注意，该方法会改变原数组。
var c = [1, 2, 3];
console.log("push c=", c.push(4, 5), c);
console.log("pop c=", c.pop(), c);
// 对空数组使用pop方法，不会报错，而是返回undefined
console.log("pop 空数组", [].pop());
//push和pop结合使用，就构成了“后进先出”的栈结构（stack）

// shift方法用于删除数组的第一个元素，并返回该元素。注意，该方法会改变原数组
console.log("shift c=", c.shift(), c);
//push和shift结合使用，就构成了“先进先出”的队列结构（queue）

// unshift 方法用于在数组的第一个位置添加元素，并返回添加新元素后的数组长度。注意，该方法会改变原数组
console.log("unshift c=", c.unshift(6), c);

// join方法以指定参数作为分隔符，将所有数组成员连接为一个字符串返回。如果不提供参数，默认用逗号分隔
// 如果数组成员是undefined或null或空位，会被转成空字符串
console.log("join c=", c.join(), c.join("!"));

// 通过call方法，这个方法也可以用于字符串或类似数组的对象
console.log("call方法", Array.prototype.join.call("Hello", "#"));
var obj = { 0: 'a', 1: 'b', length: 2 };
console.log("call方法", Array.prototype.join.call(obj, '-'));

// concat方法用于多个数组的合并。它将新数组的成员，添加到原数组成员的后部，然后返回一个新数组，原数组不变
var d = [7, 8]
console.log("concat", c.concat(d), c, d, d.concat(9, 10, 11));

// 如果数组成员包括对象，concat方法返回当前数组的一个浅拷贝。所谓“浅拷贝”，指的是新数组拷贝的是对象的引用
var obj = { a: 1 };
var oldArray = [obj];
var newArray = oldArray.concat();
obj.a = 2;
console.log("concat 浅拷贝", obj.a, newArray[0].a);

// reverse方法用于颠倒排列数组元素，返回改变后的数组。注意，该方法将改变原数组
console.log("reverse " + d, d.reverse(), d);

// slice方法用于提取目标数组的一部分，返回一个新数组，原数组不变
// slice方法的一个重要应用，是将类似数组的对象转为真正的数组
var e = ['a', 'b', { a: 1 }];
var e2 = e.slice();
e[2].a = 2;
console.log("\nslice", e.slice(0), e.slice(1), e.slice(1, 2), e.slice(2, 6), e[2].a, e2[2].a);
// 最后一个例子slice没有参数，实际上等于返回一个原数组的拷贝(浅拷贝)

// splice方法用于删除原数组的一部分成员，并可以在删除的位置添加新的数组成员，
// 返回值是被删除的元素。注意，该方法会改变原数组
// arr.splice(start, count, addElement1, addElement2, ...);
// splice的第一个参数是删除的起始位置（从0开始），第二个参数是被删除的元素个数。
// 如果后面还有更多的参数，则表示这些就是要被插入数组的新元素
console.log("splice " + c, c.splice(1, 2), c);
var f = [10, 20, 30, 40, 50, 60];
// 如果只是单纯地插入元素，splice方法的第二个参数可以设为0
console.log("splice 单纯插入", f.splice(3, 0, 70));
// 如果只提供第一个参数，等同于将原数组在指定位置拆分成两个数组
console.log("splice 拆分两个", f.splice(3), f);

// sort方法对数组成员进行排序，默认是按照字典顺序排序。排序后，原数组将被改变
// sort方法不是按照大小排序，而是按照字典顺序。
// 也就是说，数值会被先转成字符串，再按照字典顺序进行比较，所以101排在11的前面
console.log("sort", f.sort(function (a, b) { return b - a; }));

// map方法将数组的所有成员依次传入参数函数，然后把每一次的执行结果组成一个新数组返回
console.log("map " + f, f.map(function (v, i, arra) { return v ** 2; }), f);//原数组没有变化
// map方法还可以接受第二个参数，用来绑定回调函数内部的this变量
// 如果数组有空位，map方法的回调函数在这个位置不会执行，会跳过数组的空位

// forEach方法与map方法很相似，也是对数组的所有成员依次执行参数函数。
// 但是，forEach方法不返回值，只用来操作数据。
// 这就是说，如果数组遍历的目的是为了得到返回值，那么使用map方法，否则使用forEach方法
console.log("forEach", f.forEach(function (v, i, arra) { v = arra[i] + i; console.log("forEach1", v) }), f);
// forEach方法也可以接受第二个参数，绑定参数函数的this变量
// 注意，forEach方法无法中断执行，总是会将所有成员遍历完。如果希望符合某种条件时，就中断遍历，要使用for循环
// forEach方法也会跳过数组的空位(跟map函数一样)

// filter方法用于过滤数组成员，满足条件的成员组成一个新数组返回
console.log("filter " + f, f.filter(function (v, i, arra) { return i <= 1; }));
// filter方法还可以接受第二个参数，用来绑定参数函数内部的this变量

// some方法是只要一个成员的返回值是true，则整个some方法的返回值就是true，否则返回false
// every方法是所有成员的返回值都是true，整个every方法才返回true，否则返回false
// 注意，对于空数组，some方法返回false，every方法返回true，回调函数都不会执行
// some和every方法还可以接受第二个参数，用来绑定参数函数内部的this变量
console.log("some and every", f.some(function (v, i, arra) { return v > 20 })
    , f.every(function (v, i, arra) { return v > 20 }));

/**
 * reduce方法和reduceRight方法依次处理数组的每个成员，最终累计为一个值。它们的差别是，
 * reduce是从左到右处理（从第一个成员到最后一个成员），reduceRight则是从右到左（从最后一个成员到第一个成员），
 * 其他完全一样
 */
console.log("reduce =", [1, 2, 3, 4].reduce(function (累积变量, 当前变量, 当前位置, 原数组) {
    return 累积变量 ** 当前变量;
}));
console.log("reduceRight =", [1, 2, 3, 4].reduceRight(function (累积变量, 当前变量, 当前位置, 原数组) {
    return 累积变量 ** 当前变量;
}));
// 如果要对累积变量指定初值，可以把它放在reduce方法和reduceRight方法的第二个参数
// 由于空数组取不到初始值，reduce方法会报错。这时，加上第二个参数，就能保证总是会返回一个值
console.log("reduce2 =", [].reduce(function (累积变量, 当前变量, 当前位置, 原数组) {
    console.log("reduce2 function", 累积变量, 当前变量, typeof 当前变量);//空数组这里不会执行
    return 累积变量 ** 当前变量;
}, 1));//不加入第二个值会报错

// indexOf方法返回给定元素在数组中第一次出现的位置，如果没有出现则返回-1
// indexOf方法还可以接受第二个参数，表示搜索的开始位置
// lastIndexOf方法返回给定元素在数组中最后一次出现的位置，如果没有出现则返回-1
// 注意，这两个方法不能用来搜索NaN的位置，即它们无法确定数组成员是否包含NaN 判断是由严格相等
var g = [1, 2, 3, '4', 5, NaN];
console.log("indexOf", g.indexOf(4), g.indexOf(2), g.indexOf(1, 3), g.indexOf(NaN));
console.log("lastIndexOf", g.lastIndexOf(4), g.lastIndexOf(1), g.lastIndexOf(1, 3));

/**
 * 包装对象
 */
// 所谓“包装对象”，就是分别与数值、字符串、布尔值相对应的Number、String、Boolean三个原生对象。
// 这三个原生对象可以把原始类型的值变成（包装成）对象
// Number、String和Boolean如果不作为构造函数调用（即调用时不加new），
// 常常用于将任意类型的值转为数值、字符串和布尔值
var objNum = new Number(1);//使用new创建一个对象
var objNum1 = Number("1");//如果不是用new，常常用于数值转换
var objStr = new String("2");
var objBoolean = new Boolean(true);
console.log("包装对象", typeof objNum, typeof objNum1, typeof objStr, typeof objBoolean);
// 包装对象的最大目的，首先是使得 JavaScript 的对象涵盖所有的值，其次使得原始类型的值可以方便地调用某些方法
// 包装对象都有valueOf 和 toString

// 原始类型与实例对象的自动转换
// 原始类型的值，可以自动当作包装对象调用，即调用包装对象的属性和方法。
// 这时，JavaScript 引擎会自动将原始类型的值转为包装对象实例，在使用后立刻销毁实例
console.log('"abc".length =', "abc".length);//自动转对象调用length方法,用完销毁
// 自动转换生成的包装对象是只读的，无法修改。所以，字符串无法添加新属性
var str = "123";
str.x = 1;
console.log("字符串自动包装对象只读", str.x);

// 除了原生的实例方法，包装对象还可以自定义方法和属性，供原始类型的值直接调用
String.prototype.double = function () {
    return this.valueOf() + this.valueOf();
}
Number.prototype.double = function () {
    return this.valueOf() + this.valueOf();
}
console.log("自定义方法", "123".double(), (123).double());//数字必须加括号才能调用

//Boolean对象
console.log("Booean 对象", !!new Boolean(false), !!new Boolean(false).valueOf(), Boolean(false));//false转换成对象判断为true

//Number对象
console.log("Number 对象", Number(true));
console.log("Number 静态属性", Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY
    , Number.MAX_VALUE, Number.MIN_VALUE, Number.MAX_SAFE_INTEGER, Number.MIN_SAFE_INTEGER);
// toString方法可以接受一个参数，表示输出的进制
console.log("Number toString", Number.prototype.toString.call(10, 2));//默认十进制
// toString方法只能将十进制的数，转为其他进制的字符串。如果要将其他进制的数，转回十进制，需要使用parseInt方法
// toFixed方法的参数为小数位数，有效范围为0到20，超出这个范围将抛出 RangeError 错误
console.log("Number toFixed 1", Number.prototype.toFixed.call(4.554, 2));//保留两位有效数字
console.log("Number toFixed 2", Number.prototype.toFixed.call(4.555, 2));//保留两位有效数字
console.log("Number toFixed 3", Number.prototype.toFixed.call(4.556, 2));//保留两位有效数字
console.log("Number toExponential", Number.prototype.toExponential.call(4.556, 1));//转为科学计数，保留有效数字1位
// toPrecision方法的参数为有效数字的位数，范围是1到21，超出这个范围会抛出 RangeError 错误。
// toPrecision方法用于四舍五入时不太可靠，跟浮点数不是精确储存有关
console.log("Number toPrecision", Number.prototype.toPrecision.call(174.556, 1));//转为指定位数的有效数字，保留有效数字1位
// 与其他对象一样，Number.prototype对象上面可以自定义方法，被Number的实例继承

//String对象
console.log("String对象", typeof "abcd", typeof new String("abcd"));
console.log("String对象 String.fromCharCode()", String.fromCharCode(48), String.fromCharCode(97));
// 注意，该方法不支持 Unicode 码点大于0xFFFF的字符，即传入的参数不能大于0xFFFF（即十进制的 65535）
// 这种现象的根本原因在于，码点大于0xFFFF的字符占用四个字节，而 JavaScript 默认支持两个字节的字符。
// 这种情况下，必须把0x20BB7拆成两个字符表示。
// 0x20BB7
console.log("0x20BB7=", String.fromCharCode(0x20BB7), String.fromCharCode(0x20BB7) === String.fromCharCode(0x0BB7)
    , String.fromCharCode(0xD842, 0xDFB7));

var str = "123";
// 如果没有任何参数，charCodeAt返回首字符的 Unicode 码点
console.log("String对象 实例方法 ", str.length, str.charAt(0), str.charCodeAt(0), str.charCodeAt(), str.charCodeAt(-1));
// 注意，charCodeAt方法返回的 Unicode 码点不会大于65536（0xFFFF），
// 也就是说，只返回两个字节的字符的码点。如果遇到码点大于 65536 的字符（四个字节的字符），
// 必需连续使用两次charCodeAt，不仅读入charCodeAt(i)，还要读入charCodeAt(i+1)，
// 将两个值放在一起，才能得到准确的字符
console.log("中文长度", "中文".length, "ab".length, "中".charCodeAt(), String.fromCharCode(20013));

