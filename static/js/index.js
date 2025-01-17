//属性をランダムで選出
const attributes=[
    "ほのお","みず","くさ","かみなり","ノーマル","エスパー","ドラゴン","はがね","かくとう"
];
function judge(attribute){
    //属性で勝敗を判断する関数
}
const myAttributes={
    "バチンキー":"草",//1
    "ドラパルト":"エスパー",
    "ドータクン":"鋼",
    "カラサリス":"草",
    "マッギョ":"電気",//5
    "マクノシタ":"かくとう",
    "マッスグマ":"ノーマル",
    "モンメン":"草",
    "ピッピ":"エスパー",
    "プロトーガ":"水",//10
    "ランドロス":"かくとう",
    "レックウザ":"ドラゴン",
    "サンダー":"電気",
    "ビクティニ":"炎",
    "ヨワシ":"水"//15
};
var resJson;

async function sent(){
    const form = document.getElementById("form");
    const formData = new FormData(form);
    try{
        const response = await fetch("/",{
            method:"POST",
            body: formData
        });
        if (!response.ok) {
            throw new Error(`レスポンスステータス: ${response.status}`);
        }
        resJson = await response.json();
        console.log("calling")
        console.log(resJson);
        console.log("called")

        //ポケモンの属性を抽出
        const curPokeAttribute=myAttributes[resJson.poke_answer];
        //HTML要素を生成
        //resJson=JSON.parse(json);
        document.getElementById('response').innerHTML = `
                <p>これは 【 ${resJson.cloud_answer} 雲 】 です</p>
                <p>一番似ているポケモンは 【 ${resJson.poke_answer} 】 で
                【 ${curPokeAttribute} 】属性です</p>
                <img src="${resJson.image_path}" alt="関連ポケモンの画像">
        `;
    }catch(error){
        console.log("エラー");
    }
}

//画像が送信されたら呼ばれる関数
console.log("start");

const randomAttribute=attributes[Math.floor(Math.random()*(attributes.length))];
document.getElementById("mission").textContent=`${randomAttribute}タイプのポケモンに似た雲の写真を撮ろう！`;
