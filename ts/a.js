;
// class DllCls{
//     init(flag:boolean):boolean{
//         return true;
//     }
// }
// namespace Test{
//     enum Color {Red, Green, Blue };
// }
var Color;
(function (Color) {
    Color[Color["Red"] = 0] = "Red";
    Color[Color["Green"] = 1] = "Green";
    Color[Color["Blue"] = 2] = "Blue";
})(Color || (Color = {}));
;
class UserData {
    //strLength: number = (this.someValue as string).length; // 并不能用
    constructor() {
        this.list3 = [1, "2", true];
        //void //指定不返回
        //undefined //未定义
        //null      //空值
        //断言 as
        this.someValue = "this is a string";
        console.log("constructor UserData");
        /**
         * let比var多了
         *  作用域之外销毁的功能
         *  屏蔽重定义
         *  块级作用域变量的获取
         *
         * 不过我们尽量少用屏蔽功能，否则容易看不懂代码
         */
        let temp1 = true; //变量赋值，
        const temp2 = 1; //常量赋值
        //解构数组
        let arra = [1, 2];
        let [first, second] = arra;
        console.log("解构数组:" + first + "," + second);
        try {
            throw "oh no!";
        }
        catch (e) {
            console.log("Oh well.");
        }
    }
}
class UserMath extends UserData {
    //readonly cls_type:number = 1;//tsc 编译成js 报错？？？
    constructor() {
        super();
        console.log("constructor UserMath");
    }
    getMath(add) {
        let temp = this.flag ? add.valueOf() : 0; //三目运算符
        return this.math.valueOf() + temp;
    }
    /**
     * getLevel
     */
    getLevel() {
        if (this.math >= 90)
            return "优秀";
        else if (this.math >= 75)
            return "良";
        else if (this.math >= 60)
            return "及格";
        else
            return "不及格";
    }
    /**
     * getPP
     */
    getPP() {
        switch (this.getLevel()) {
            case "优秀":
                return "好";
            default:
                return "不好";
        }
    }
}
UserMath.cls = "数学";
for (let i = 0; i < 10; i++) {
    console.log("console1:" + i);
}
let j = 0;
while (j < 10) {
    console.log("console2:" + j);
    j++;
}
let obj1 = new UserMath();
