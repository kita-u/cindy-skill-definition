`---
name: cindycs-csinit-query-url-compact
description: >-
  Generates browseable Cindy.js URLs (cindy_csinit_query_plus.html?csinit=...) using create() commands. 
  Self-contained compact version including all reference documentation and sample constructions. 
  Use when the user wants to generate a URL for geometry construction without needing external reference files.
---

# Cindy.js クエリ URL 生成 (Compact)

## 本スキルについて

このスキルは、**`cindy_csinit_query_plus.html`** をゲートウェイとして、Cindy.js の作図をブラウザで即座に表示するための URL を生成します。

### 成果物
- **URL 文字列**: `cindy_csinit_query_plus.html?csinit=...`（CindyScript を `encodeURIComponent` したもの）

## ワークフロー

1. **作図指示を解釈**し、後述のリファレンスを参照して `create` 命令の列を組み立てる。
2. 末尾に **`allelements()`** を追加する。
3. CindyScript 全体を **`encodeURIComponent`** し、ベース URL と連結する。
   - `https://kita-u.github.io/cindy-skill-definition/cindy_csinit_query_plus.html?csinit=<encoded_script>`
4. 必要に応じて `&title=<encoded_title>` を付与する。

---

## リファレンス: `create` 命令一覧

作図には以下の命令を使用してください。

| 命令・構文 | 内容 |
|:---|:---|
| `create(["A"],"Free",[[x,y,1]])` | 動点 A を xy 座標 (x, y) に作成 |
| `create(["a"],"Segment",[A,B])` | 点 A と B を結ぶ線分 a を作成 |
| `create(["a"],"Join",[A,B])` | 点 A と B を通る直線 a を作成 |
| `create(["X"],"CircleMP",[A,B])` | 中心 A、点 B を通る円 X を作成 |
| `create(["M"],"Meet",[a,b])` | 直線 a, b の交点 M を作成 |
| `create(["P","Q"],"IntersectionCircleCircle",[X,Y])` | 円 X, Y の交点 P, Q を作成 (順序不定) |
| `create(["P","Q"],"IntersectionConicLine",[X,a])` | 円 X と直線 a の交点 P, Q を作成 (順序不定) |
| `create(["Q"],"OtherIntersectionCL",[X,a,P])` | 円 X と直線 a の交点のうち、P 以外の点 Q を作成 |
| `create(["Q"],"OtherIntersectionCC",[X,Y,P])` | 円 X と円 Y の交点のうち、P 以外の点 Q を作成 |
| `create(["C"],"Mid",[A,B])` | 点 A, B の中点 C を作成 |
| `create(["b"],"Orthogonal",[a,C])` | 点 C を通り、直線 a に直交する 直線 b を作成 |

### 補助関数: `nearpoint`
交点の順序を特定したい場合は、以下の定義を `csinit` の冒頭に含めて使用します。
create命令で IntersectionCircleCircle, IntersectionConicLine を使ったときは、点 P, Q の順番は不定です。
P, Q のどちらが必要な点なのかを判定するために、必ず nearpoint() または別の手段を使って P, Q のどちら
が必要な点かを判定して、P, Q のうちどちらが必要な点を使うようにしてください。
```cindyscript
nearpoint(p1,p2,a):= if (dist(p1.xy,a.xy)<dist(p2.xy,a.xy), p1, p2);
```

### nearpoint() で使う点の作成
nearpoint(p1,p2,a) で使う点 a は次の命令で作成できます。
a = [ aのx座標, aのy座標 ]

### 座標の取り出し
点Aのx座標は A.x で取り出せます。点Aのy座標は A.y で取り出せます。
A.xy は [ A.x, A.y ] の形のベクトルを返します。

### 演算子
CindyJS では数値の加減乗除は +, -, *, / を使います。
u, v がベクトルのときは u+v,  u-v が使えます。
u*v は u と v の内積を返します。

### 表示・非表示の切り替え
P を非表示にするには P.visible = false;
P を表示するには P.visible = true;
デフォールトでは P.visible は true になっている。

### 色の変更
P.color = [r,g,b] で P の色を設定する。
r,g,b は RGB の色の強さを表し、0 から 1 の数値である。

### ラベルの設定
P.label = "ラベル名"
で P のラベルを設定する。

### 点の大きさ、線の太さ
P.size = 点の大きさ（または線の太さ）
で点の大きさや線の太さを設定できます。
点の大きさ（または太さ）は整数値で与え、デフォールトは 4 です。

## 注意事項
- **命名規則**: 変数名と関数名には半角英数字のみを使用してください（アンダースコア不可）。
- 変数名と関数名で perpB_AM などのアンダースコアを入れた名前は決して使わない。
- **作図の完成を優先**: 長さを理由に `create` 命令を省略・短縮しない。指示どおりの図形を最後まで組み立てる。
- **URL 長さ**: 現代のブラウザでは URL はおおよそ **8000 文字程度**まで扱える。エンコード後の URL が 8000 文字を超えるほど極端に長い場合のみ、HTML ファイル化を提案する。


---

## ゲートウェイ HTML (`cindy_csinit_query_plus.html`)

この URL 形式を動かすための最小構成の HTML です。ユーザーが自身のサーバー等に配置する必要があります。

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Cindy.js（クエリ csinit）</title>
    <link rel="stylesheet" href="https://cindyjs.org/dist/v0.8/CindyJS.css">
    <script type="text/javascript" src="https://cindyjs.org/dist/v0.8/Cindy.js"></script>
    <script id="csinit" type="text/x-cindyscript">allelements()</script>
    <script type="text/javascript">
    (function () {
      var params = new URLSearchParams(window.location.search);
      var enc = params.get("csinit");
      if (enc) {
        document.getElementById("csinit").textContent = enc;
      }
      var t = params.get("title");
      if (t) document.title = t;
    })();
    var cdy = CindyJS({
      scripts: "cs*",
      defaultAppearance: { dimDependent: 0.7, fontFamily: "sans-serif", lineSize: 1, pointSize: 5.0, textsize: 12.0 },
      ports: [{ width: 680, height: 337, id: "CSCanvas", transform: [{ visibleRect: [-8.5, 6.5, 8.5, -5.5] }], background: "rgb(168,176,192)" }]
    });
    </script>
</head>
<body><div id="CSCanvas"></div></body>
</html>
```

---

## 作図サンプル集 (CindyScript)

### 1. 正三角形
```cindyscript
create(["A"],"Free",[[0,0,1]]);
create(["B"],"Free",[[4,0,1]]);
create(["X"],"CircleMP",[A,B]);
create(["Y"],"CircleMP",[B,A]);
create(["C","D"],"IntersectionCircleCircle",[X,Y]);
if (C.y < D.y, C = D);  // y座標が上の点をCとする。
create(["s1"],"Segment",[A,B]);
create(["s2"],"Segment",[B,C]);
create(["s3"],"Segment",[A,C]);
allelements();
```

### 2. 角の二等分線 (角 AOB)
```cindyscript
nearpoint(p1,p2,a):= if (dist(p1.xy,a.xy)<dist(p2.xy,a.xy), p1, p2);
create(["O"],"Free",[[0,0,1]]);
create(["A"],"Free",[[5,0,1]]);
create(["B"],"Free",[[2,3,1]]);
create(["rayOA"],"Join",[O,A]);
create(["rayOB"],"Join",[O,B]);
create(["circ1"],"CircleMP",[O,A]);
create(["P","Q"],"IntersectionConicLine",[circ1,rayOB]);
C = nearpoint(P,Q,B);
create(["circ2"],"CircleMP",[A,O]);
create(["circ3"],"CircleMP",[C,O]);
create(["D"],"OtherIntersectionCC",[circ2,circ3,O]);
create(["bis"],"Join",[O,D]);
allelements();
```

### 3. 線分の垂直二等分線と中点
```cindyscript
nearpoint(p1,p2,a):= if (dist(p1.xy,a.xy)<dist(p2.xy,a.xy), p1, p2);
create(["A"],"Free",[[1,1,1]]);
create(["B"],"Free",[[4,3,1]]);
create(["a"],"Join",[A,B]);
create(["X"],"CircleMP",[A,B]);
create(["Y"],"CircleMP",[B,A]);
create(["P","Q"],"IntersectionCircleCircle",[X,Y]);
create(["b"],"Join",[P,Q]);
create(["M"],"Meet",[a,b]);
allelements();
```

### 4. タレスの定理 (∠APB=90°)
```cindyscript
nearpoint(p1,p2,a):= if (dist(p1.xy,a.xy)<dist(p2.xy,a.xy), p1, p2);
create(["A"],"Free",[[-2,0,1]]);
create(["B"],"Free",[[2,0,1]]);
create(["a"],"Segment",[A,B]);
create(["M"],"Mid",[A,B]);
create(["cAB"],"CircleMP",[M,A]);
create(["C"],"Free",[[3,3,1]]);
create(["sMC"],"Join",[M,C]);
create(["P","Q"],"IntersectionConicLine",[cAB,sMC]);
D = nearpoint(P,Q,C);  //  点C に近い方を点Dにとる
create(["sAP"],"Segment",[A,D]);
create(["sBP"],"Segment",[B,D]);
allelements();
```

### 5. 正五角形
```cindyscript
create(["O"],"Free",[[0,0,1]]);
create(["A"],"Free",[[5,0,1]]);
create(["k"],"CircleMP",[O,A]);
create(["dia"],"Join",[O,A]);
create(["B"],"OtherIntersectionCL",[k,dia,A]);
create(["perp"],"Orthogonal",[dia,O]);
create(["Pref"],"Free",[[1,-8,1]]);
create(["C"],"OtherIntersectionCL",[k,perp,Pref]);
create(["M"],"Mid",[O,B]);
create(["kM"],"CircleMP",[M,C]);
create(["N"],"OtherIntersectionCL",[kM,dia,B]);
create(["kCN"],"CircleMP",[C,N]);
create(["V1"],"OtherIntersectionCC",[k,kCN,C]);
create(["k1"],"CircleMP",[V1,C]);
create(["V2"],"OtherIntersectionCC",[k,k1,C]);
create(["k2"],"CircleMP",[V2,V1]);
create(["V3"],"OtherIntersectionCC",[k,k2,V1]);
create(["k3"],"CircleMP",[V3,V2]);
create(["V4"],"OtherIntersectionCC",[k,k3,V2]);
create(["e0"],"Segment",[C,V1]);
create(["e1"],"Segment",[V1,V2]);
create(["e2"],"Segment",[V2,V3]);
create(["e3"],"Segment",[V3,V4]);
create(["e4"],"Segment",[V4,C]);
allelements()
```


---

## 応答形式（必須）

ユーザーへの返答は、**次の2つのコードブロックのみ**とする。前後に説明文・コメント・箇条書きを付けない。

```cindyscript
（CindyScript 全文。末尾は allelements()）
```

```URL
https://kita-u.github.io/cindy-skill-definition/cindy_csinit_query_plus.html?csinit=（CindyScript を encodeURIComponent した文字列）
```

ベース URL は必ず `https://kita-u.github.io/cindy-skill-definition/cindy_csinit_query_plus.html` を使う。
