//属性をランダムで選出
const attributes=[
    "ほのお","みず","くさ","でんき","ノーマル","エスパー","ドラゴン","はがね","かくとう"
];
function judge(attribute){
    //属性で勝敗を判断する関数
}
const myAttributes={
    "バチンキー":"くさ",//1
    "ドラパルト":"エスパー",
    "ドータクン":"はがね",
    "カラサリス":"くさ",
    "マッギョ":"でんき",//5
    "マクノシタ":"かくとう",
    "マッスグマ":"ノーマル",
    "モンメン":"くさ",
    "ピッピ":"エスパー",
    "プロトーガ":"みず",//10
    "ランドロス":"かくとう",
    "レックウザ":"ドラゴン",
    "サンダー":"でんき",
    "ビクティニ":"ほのお",
    "ヨワシ":"みず"//15
};

const randomAttribute=attributes[Math.floor(Math.random()*(attributes.length))];
document.getElementById("mission").textContent=`${randomAttribute}タイプのポケモンに似た雲の写真を撮ろう！`;
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
                【 ${curPokeAttribute} 】タイプです</p>
                <h2 id="success" style="display:none;">ミッション達成！</h2>
                <h2 id="fail" style="display:none;">ミッション失敗...</h2>
                <img src="${resJson.image_path}" alt="関連ポケモンの画像">
        `;
        console.log(form);
        if(curPokeAttribute===randomAttribute){
            //フォームを非表示
            form.style.display="none";
            document.getElementById("instruction").style.display="none";
            //ミッション成功のセリフ
            document.getElementById("success").style.display="block";
        }else{
            //ミッション失敗のセリフ
            document.getElementById("fail").style.display="block";
        }
    }catch(error){
        console.log("エラー");
    }
}

//画像が送信されたら呼ばれる関数
console.log("start");
