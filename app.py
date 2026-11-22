#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""honmenquiz — 本免学科試験対策 ○×カード形式クイズ.

単一ファイル Flask アプリ。問題はすべて自作の学習用問題（120問）で、
公式の試験問題ではありません。本免学科試験のイラスト問題（危険予測）は
含みません。

目次（Unit 一覧）
  Unit 1: 問題データ（カテゴリ別 ○×問題 120問）
  Unit 2: Web アプリ（ルート定義・画面表示）
"""

from flask import Flask, jsonify, render_template_string

# ============================================================
# Unit 1: 問題データ
#   answer: true = 問題文が正しい（○）, false = 問題文が誤り（×）
# ============================================================
QUESTIONS = [
    # ---- 法規の基礎 ----
    {"q": "運転免許を受けずに自動車を運転することは、無免許運転として処罰の対象になる。", "answer": True, "explanation": "免許を受けていない者が自動車等を運転すると無免許運転となり、罰則のほか免許取得の欠格期間が科されることがあります。", "category": "法規の基礎"},
    {"q": "運転免許証は、有効期間が過ぎても、更新手続をするまでの間は効力がある。", "answer": False, "explanation": "有効期間を過ぎた免許証は失効します。更新を忘れたまま運転すると無免許運転になるおそれがあります。", "category": "法規の基礎"},
    {"q": "歩行者の側方を通過するときは、安全な間隔を保ち、安全な間隔が保てない場合は徐行しなければならない。", "answer": True, "explanation": "歩行者の通行を妨げないよう、安全な間隔を保てないときは徐行することが義務付けられています。", "category": "法規の基礎"},
    {"q": "青色の信号は、車両に「進め」と命令する信号である。", "answer": False, "explanation": "青信号は「進むことができる」という意味で、命令ではありません。交通の状況によっては進まず止まることも必要です。", "category": "法規の基礎"},
    {"q": "赤色の信号では、車両は停止位置を越えて進行してはならない。", "answer": True, "explanation": "赤信号は「停止」を意味します。停止位置を越えて進むことはできません。", "category": "法規の基礎"},
    {"q": "黄色の信号で停止位置に近づいているときは、安全に止まれない場合でも急ブレーキをかけて必ず止まらなければならない。", "answer": False, "explanation": "黄色信号では原則停止ですが、安全に停止できない場合はそのまま進むことができます。急ブレーキは追突の危険があります。", "category": "法規の基礎"},
    {"q": "警察官が腕を垂直に上げている手信号は、対面する交通に対しては赤信号とほぼ同じ意味である。", "answer": True, "explanation": "警察官の手信号が信号機の信号と異なるときは手信号が優先します。腕を垂直に上げた姿勢は、対面する交通には赤信号と同義です。", "category": "法規の基礎"},
    {"q": "交通整理の行われていない交差点では、右方から進行してくる車両が優先する。", "answer": False, "explanation": "優先関係が明らかでない交差点では、左方から進行してくる車両の進行を妨げてはなりません（左方優先）。", "category": "法規の基礎"},
    {"q": "道路外の施設に出入りするために歩道を横切るときは、歩道の直前で一時停止し、歩行者の通行を妨げてはならない。", "answer": True, "explanation": "歩道を横切る場合は直前で一時停止し、歩行者がいるときはその通行を妨げてはなりません。", "category": "法規の基礎"},
    {"q": "徐行とは、時速10キロメートル以下で走行することと決められている。", "answer": False, "explanation": "徐行とは「車両等が直ちに停止することができるような速度」で進行することです。具体的な数値は定められていません。", "category": "法規の基礎"},
    {"q": "車両は、道路の中央から左の部分を通行するのが原則である。", "answer": True, "explanation": "日本では左側通行が原則で、車両は道路の左側部分を通行します。", "category": "法規の基礎"},
    {"q": "対向車と行き違うときは、道路の中央に寄って通行するのが安全である。", "answer": False, "explanation": "行き違うときは、道路の左側端に寄って通行します。中央に寄ると対向車と接触する危険が高まります。", "category": "法規の基礎"},
    {"q": "他の車両を追い越すときは、原則として、追い越される車両の右側を通行する。", "answer": True, "explanation": "追い越しは原則として右側から行います。左側から追い越せるのは、前の車両が右折のため中央に寄っている場合など限られた場合だけです。", "category": "法規の基礎"},
    {"q": "前の車両が右折するために道路の中央に寄っているときは、その左側を通行して追い越すことはできない。", "answer": False, "explanation": "前の車両が右折しようとして中央に寄っている場合は、その左側を通行して追い越すことができます。", "category": "法規の基礎"},
    {"q": "交差点と、その手前30メートル以内の場所では、原則として他の車両を追い越してはならない。", "answer": True, "explanation": "交差点とその手前30メートル以内は追い越し禁止場所です（優先道路を通行している場合などの例外を除きます）。", "category": "法規の基礎"},
    {"q": "踏切とその手前30メートル以内の場所では、追い越しは禁止だが追い抜きはできる。", "answer": False, "explanation": "踏切とその手前30メートル以内では、追い越しも追い抜きも禁止されています。", "category": "法規の基礎"},
    {"q": "坂の頂上付近や、勾配の急な下り坂では、他の車両を追い越してはならない。", "answer": True, "explanation": "見通しの悪い坂の頂上付近や急な下り坂は、追い越し禁止場所に定められています。", "category": "法規の基礎"},
    {"q": "トンネルの中では、車両通行帯が設けられている場合でも、常に追い越しが禁止されている。", "answer": False, "explanation": "追い越しが禁止されるのは車両通行帯の設けられていないトンネルです。車両通行帯があるトンネルでは追い越しができます。", "category": "法規の基礎"},
    {"q": "横断歩道と、その手前30メートル以内の場所では、原則として追い越しも追い抜きも禁止されている。", "answer": True, "explanation": "横断歩道とその手前30メートル以内は、歩行者保護のため追い越し・追い抜きの禁止場所です。", "category": "法規の基礎"},
    {"q": "歩行者が横断歩道を横断しているときは、車両は徐行して歩行者の前を通過することができる。", "answer": False, "explanation": "横断歩道を横断中、または横断しようとする歩行者がいるときは、横断歩道の直前で一時停止しなければなりません。", "category": "法規の基礎"},
    {"q": "横断歩道のない交差点やその付近を歩行者が横断しているときは、その通行を妨げてはならない。", "answer": True, "explanation": "横断歩道がない場所でも、横断中の歩行者の通行を妨げてはなりません。", "category": "法規の基礎"},
    {"q": "横断歩道に接近するときは、歩行者の有無にかかわらず、必ず一時停止しなければならない。", "answer": False, "explanation": "横断歩道に接近するときは、横断する歩行者がいるかどうか明らかでない場合に、直前で停止できるような速度で進行します。必ず一時停止するわけではありません。", "category": "法規の基礎"},
    {"q": "幼児や児童、身体の不自由な人などが通行しているときは、一時停止するか徐行して、安全に通行できるようにしなければならない。", "answer": True, "explanation": "保護者に同伴されていない幼児や、身体障害者用車いすで通行する人などに対しては、一時停止または徐行して安全を図ります。", "category": "法規の基礎"},
    {"q": "安全地帯に歩行者がいるときは、その側方を徐行せずに通過することができる。", "answer": False, "explanation": "安全地帯に歩行者がいるときは、その側方を徐行して通過しなければなりません。", "category": "法規の基礎"},
    # ---- 標識・標示 ----
    {"q": "一時停止の標識は、赤色の逆三角形の形をしている。", "answer": True, "explanation": "一時停止（止まれ）の標識は、頂点が下を向いた赤い逆三角形で、他の標識と区別しやすい形になっています。", "category": "標識・標示"},
    {"q": "道路に描かれたダイヤ形の標示は、この先に横断歩道または自転車横断帯があることを示している。", "answer": True, "explanation": "ダイヤマークは横断歩道等の手前30〜50メートルに設置され、運転者に注意を促す標示です。", "category": "標識・標示"},
    {"q": "ダイヤ形の標示は、その場所に駐車してよいことを示している。", "answer": False, "explanation": "ダイヤマークは駐車の許可ではなく、この先の横断歩道・自転車横断帯を知らせる標示です。", "category": "標識・標示"},
    {"q": "黄色の実線の中央線は、追い越しのために反対側へはみ出して通行してはならないことを示している。", "answer": True, "explanation": "黄色の実線は「はみ出し通行禁止」を表します。追い越しのためにはみ出すことはできません。", "category": "標識・標示"},
    {"q": "白色の実線の中央線も、黄色の実線と同じく、追い越しのためにはみ出すことは一切できない。", "answer": False, "explanation": "白色の実線の中央線は、追い越しのためにはみ出して通行することができます（黄色の実線とは意味が異なります）。", "category": "標識・標示"},
    {"q": "補助標識は、本標識が示す規制などの内容を補足するために取り付けられる。", "answer": True, "explanation": "補助標識は、規制の時間・車両の種類・区間などを補足するもので、本標識とあわせて読みます。", "category": "標識・標示"},
    {"q": "「車両通行止め」の標識がある道路は、歩行者も通行することができない。", "answer": False, "explanation": "車両通行止めは車両だけを対象とし、歩行者は通行できます。歩行者も止める場合は「歩行者通行止め」の標識があります。", "category": "標識・標示"},
    {"q": "「歩行者通行止め」の標識がある場所は、歩行者も通行することができない。", "answer": True, "explanation": "歩行者通行止めの標識は、歩行者の通行そのものを禁止するものです。", "category": "標識・標示"},
    {"q": "一方通行の道路では、自転車などの軽車両も、指定された方向と反対向きに通行することはできない。", "answer": True, "explanation": "自転車も車両の一種として一方通行の規制を受けます（「自転車を除く」の補助標識がある場合を除きます）。", "category": "標識・標示"},
    {"q": "「徐行」の標識は、徐行しなければならない区間の終わりを示すものである。", "answer": False, "explanation": "徐行の標識は、徐行しなければならない場所であることを示す規制標識です。区間の終わりを示すものではありません。", "category": "標識・標示"},
    {"q": "標識による最高速度の指定がない一般の道路では、普通自動車の法定最高速度は時速50キロメートルである。", "answer": False, "explanation": "一般道路での普通自動車の法定最高速度は時速60キロメートルです。", "category": "標識・標示"},
    {"q": "歩行者専用道路の標識がある道路では、原則として車両は通行できない。", "answer": True, "explanation": "歩行者専用道路は歩行者のための道路で、許可を受けた車両などを除き車両は通行できません。", "category": "標識・標示"},
    {"q": "「転回禁止」の標識がある場所では、右折や左折も禁止される。", "answer": False, "explanation": "転回禁止はUターンだけを禁止するもので、右折や左折は禁止されません。", "category": "標識・標示"},
    {"q": "「追越し禁止」の標識は追い越しを禁止するものであり、追い抜きまで禁止するものではない。", "answer": True, "explanation": "標識による規制は「追い越し」の禁止です。追い抜きは禁止されませんが、安全な方法で行う必要があります。", "category": "標識・標示"},
    {"q": "黄色の灯火の点滅信号は、車両が徐行しなければならないことを意味する。", "answer": False, "explanation": "黄色の点滅は「他の交通に注意して進むことができる」という意味です。徐行の義務まではありませんが、十分な注意が必要です。", "category": "標識・標示"},
    {"q": "赤色の灯火の点滅信号は、車両が一時停止して安全確認をしなければならないことを意味する。", "answer": True, "explanation": "赤色の点滅は一時停止の意味です。停止位置で止まり、左右の安全を確認してから進みます。", "category": "標識・標示"},
    {"q": "警戒標識は、主としてひし形で、黄色の地に黒色の記号が描かれている。", "answer": True, "explanation": "警戒標識は道路の危険な場所などを知らせるもので、ひし形・黄色地が基本の形です。", "category": "標識・標示"},
    {"q": "規制標識は、主としてひし形の形をしている。", "answer": False, "explanation": "規制標識は主として円形です。ひし形は警戒標識の形です。", "category": "標識・標示"},
    {"q": "案内標識は、主として四角形で、青色や緑色が使われている。", "answer": True, "explanation": "案内標識は地名や方向、距離などを示すもので、長方形で青色・緑色が使われます。", "category": "標識・標示"},
    {"q": "指示標識は、赤色を主として使った標識である。", "answer": False, "explanation": "指示標識は青色の地に白色の記号が基本で、横断歩道や安全地帯などを示します。", "category": "標識・標示"},
    {"q": "「横断歩道」の指示標識は、青色の地に白色で歩行者の図が描かれている。", "answer": True, "explanation": "横断歩道の指示標識は青地に白い歩行者の図柄です。路面のしま模様の標示とあわせて設置されます。", "category": "標識・標示"},
    {"q": "道路の左側端に沿って引かれた黄色の破線の標示は、駐車が禁止されていることを示している。", "answer": True, "explanation": "黄色の破線は駐車禁止、黄色の実線は駐停車禁止を示す標示です（駐車禁止の場所でも停車は可能です）。", "category": "標識・標示"},
    {"q": "安全地帯は、路面電車の乗降客などの安全を守るための場所で、車両がその中を通行することはできない。", "answer": True, "explanation": "安全地帯は歩行者の安全のための区域で、車両は進入できません。歩行者がいるときは側方を徐行します。", "category": "標識・標示"},
    {"q": "停止線は、車両の後輪が越えてはならないことを示す線である。", "answer": False, "explanation": "停止線は、車両の前部（前端）が越えてはならない線です。停止するときは停止線の直前で止まります。", "category": "標識・標示"},
    # ---- 高速道路 ----
    {"q": "高速自動車国道の本線車道では、普通自動車の最高速度は時速100キロメートルである。", "answer": True, "explanation": "高速自動車国道の本線車道での普通自動車の法定最高速度は100km/hです（標識で指定がある場合はそれに従います）。", "category": "高速道路"},
    {"q": "高速道路では、すべての自動車の最高速度は時速120キロメートルと定められている。", "answer": False, "explanation": "普通自動車でも法定最高速度は100km/hです。一部の区間で120km/hが指定されることはありますが、全車一律ではありません。", "category": "高速道路"},
    {"q": "高速自動車国道の本線車道では、最低速度は時速50キロメートルと定められている。", "answer": True, "explanation": "本線車道には最低速度50km/hの定めがあり、これより遅い速度では走行できません（故障などのやむを得ない場合を除きます）。", "category": "高速道路"},
    {"q": "高速道路の加速車線や減速車線にも、最低速度50キロメートルの定めがある。", "answer": False, "explanation": "最低速度の定めがあるのは本線車道だけです。加速車線・減速車線には最低速度の定めはありません。", "category": "高速道路"},
    {"q": "高速道路では、大型貨物自動車の最高速度は時速80キロメートルである。", "answer": True, "explanation": "大型貨物自動車や大型特殊自動車、けん引自動車の最高速度は80km/hです。", "category": "高速道路"},
    {"q": "排気量125cc以下の普通自動二輪車は、高速道路を通行することができない。", "answer": True, "explanation": "高速道路を通行できる二輪車は125ccを超えるものに限られます。原動機付自転車やミニカーも通行できません。", "category": "高速道路"},
    {"q": "原動機付自転車は、高速道路の路肩を通行すれば高速道路を使うことができる。", "answer": False, "explanation": "原動機付自転車は高速道路を一切通行できません。路肩の通行も認められていません。", "category": "高速道路"},
    {"q": "高速道路の本線に合流するときは、本線を通行している車両の進行を妨げてはならない。", "answer": True, "explanation": "合流する側が本線の流れに合わせます。本線の車両に減速や進路変更を強いるような合流は禁止です。", "category": "高速道路"},
    {"q": "高速道路で合流するときは、本線を通行する車両の方が速度を落として合流車両を入れるのが原則である。", "answer": False, "explanation": "本線の車両に優先権があり、合流する車両が加速車線で十分に加速して、本線の進行を妨げないように合流します。", "category": "高速道路"},
    {"q": "高速道路の本線車道では、転回（Uターン）や後退をしてはならない。", "answer": True, "explanation": "本線車道での転回・後退・横断は禁止されています。出口を通り過ぎたら次の出口まで進みます。", "category": "高速道路"},
    {"q": "出口を通り過ぎてしまったときは、後続車がいなければ路肩を後退して出口まで戻ることができる。", "answer": False, "explanation": "高速道路での後退は路肩でも禁止です。通り過ぎた場合は次の出口で降りてください。", "category": "高速道路"},
    {"q": "高速道路で故障などのためやむを得ず停止するときは、停止表示器材を車両の後方に置かなければならない。", "answer": True, "explanation": "高速道路で停止する場合は、三角表示板などの停止表示器材を後方に設置する義務があります。", "category": "高速道路"},
    {"q": "停止表示器材は、夜間に停止するときだけ置けばよく、昼間は置かなくてよい。", "answer": False, "explanation": "停止表示器材の設置は昼夜を問いません。昼間でも車両の後方に置く必要があります。", "category": "高速道路"},
    {"q": "高速道路の非常電話は、おおむね1キロメートル間隔で設置されている。", "answer": True, "explanation": "非常電話は本線では約1km間隔、トンネル内では約200m間隔で設置され、係員と直接通話できます。", "category": "高速道路"},
    {"q": "高速道路を時速100キロメートルで走行するときは、約100メートルの車間距離を保つことが目安とされている。", "answer": True, "explanation": "車間距離の目安は「速度の数字とほぼ同じメートル数」で、100km/hなら約100m、80km/hなら約80mです。", "category": "高速道路"},
    {"q": "雨の日は路面が滑りやすいが、車間距離は晴れの日と同じでよい。", "answer": False, "explanation": "雨天時は制動距離が延びるため、晴れの日より車間距離を長く（およそ2倍を目安に）取る必要があります。", "category": "高速道路"},
    {"q": "高速道路で自動二輪車に二人乗りをするには、運転者が20歳以上で、二輪免許を受けて3年以上でなければならない。", "answer": True, "explanation": "高速道路での二輪車の二人乗りは、年齢20歳以上・免許取得3年以上が条件です（一般道の二人乗りとは条件が異なります）。", "category": "高速道路"},
    {"q": "高速道路では、原則として左側の走行車線を通行し、追い越しをするときに追越車線を使う。", "answer": True, "explanation": "追越車線は追い越しのための車線です。追い越しが終わったら走行車線に戻ります。", "category": "高速道路"},
    {"q": "高速道路に入る前の点検は、最初のサービスエリアに入ってから行えばよい。", "answer": False, "explanation": "燃料・タイヤ・ライトなどの点検は、高速道路に入る前に済ませておきます。本線での停止は大変危険です。", "category": "高速道路"},
    {"q": "高速道路では、歩行者は路肩に限って通行することができる。", "answer": False, "explanation": "歩行者は高速道路を一切通行できません（故障時に車外へ避難する場合などの緊急時を除きます）。", "category": "高速道路"},
    {"q": "高速道路で故障した車両は、ロープなどでけん引して高速道路を通行させることができる。", "answer": True, "explanation": "故障車のけん引は高速道路でも認められています。ロープは5メートル以内、白い布（0.3メートル四方以上）を付けるなどの決まりを守ります。", "category": "高速道路"},
    {"q": "高速道路の料金所では、どのレーンでも止まらずにそのまま通過してよい。", "answer": False, "explanation": "料金所では、ETC専用レーンでETCを使う場合などを除き、一時停止して料金を支払います。通過方法はレーンの表示に従ってください。", "category": "高速道路"},
    {"q": "高速道路の出口では、減速車線に入ってから十分に速度を落とすようにする。", "answer": True, "explanation": "本線車道で急に減速すると追突の危険があります。減速は減速車線に入ってから行います。", "category": "高速道路"},
    {"q": "高速道路のトンネル内では、昼間であれば前照灯を点灯しなくてよい。", "answer": False, "explanation": "トンネル内は昼間でも暗いため、前照灯を点灯して自車の存在を周囲に知らせます。", "category": "高速道路"},
    # ---- 安全運転 ----
    {"q": "酒気を帯びて運転するおそれがある人に車両を提供した人も、処罰の対象になる。", "answer": True, "explanation": "飲酒運転は本人だけでなく、車両の提供者、酒類の提供者、要求・依頼して同乗した人も処罰されます。", "category": "安全運転"},
    {"q": "ビールをコップ1杯飲んだ程度であれば、運転しても飲酒運転にはならない。", "answer": False, "explanation": "酒量の多少にかかわらず、酒を飲んだときは運転してはなりません。「少しなら大丈夫」という考えが重大事故につながります。", "category": "安全運転"},
    {"q": "運転中に携帯電話を手に持って通話したり、画面を注視したりすることは禁止されている。", "answer": True, "explanation": "運転中の携帯電話等の使用は、通話も画面の注視も禁止され、罰則と違反点数の対象です。", "category": "安全運転"},
    {"q": "他の車両の通行を妨害する目的で急な割り込みや幅寄せなどをする「あおり運転」は、妨害運転罪として重く処罰される。", "answer": True, "explanation": "妨害運転（あおり運転）は、免許取消しや懲役刑の対象となる重大な違反です。", "category": "安全運転"},
    {"q": "眠気を感じても、窓を開けて換気すれば、そのまま運転を続けてよい。", "answer": False, "explanation": "眠気を感じたら運転を続けてはいけません。安全な場所に停車して休憩や仮眠を取ることが必要です。", "category": "安全運転"},
    {"q": "雨の日に水たまりの上を高速で走ると、タイヤと路面の間に水の膜ができてハンドルやブレーキが効かなくなることがある。", "answer": True, "explanation": "ハイドロプレーニング現象です。雨天時は速度を落とし、タイヤの溝や空気圧にも注意します。", "category": "安全運転"},
    {"q": "夜間、対向車と行き違うときは、前照灯を下向き（減光）にして相手をまぶしくさせないようにする。", "answer": True, "explanation": "対向車や先行車があるときは前照灯を減光します。まぶしさは相手の視力を一時的に奪い、危険です。", "category": "安全運転"},
    {"q": "夜間は、対向車や先行車がいないときでも、前照灯を常に下向きにしておかなければならない。", "answer": False, "explanation": "夜間の前照灯は上向きが原則です。対向車と行き違うときや先行車の直後では下向きに切り替えます。", "category": "安全運転"},
    {"q": "運転席からは車の周囲に死角があるため、発進する前に車の周囲を直接目で確認することが大切である。", "answer": True, "explanation": "特に車の前後や左側方には大きな死角があります。乗車前・発進前の周囲確認が事故防止につながります。", "category": "安全運転"},
    {"q": "大型車が左折するときは内輪差が生じ、後輪が前輪より内側を通るため、二輪車や歩行者の巻き込みに注意が必要である。", "answer": True, "explanation": "内輪差は車体が長い車ほど大きくなります。左折時は左後方の安全確認が欠かせません。", "category": "安全運転"},
    {"q": "右折するとき、対向車がまだ遠くにいる場合は、その前を急いで右折しても安全である。", "answer": False, "explanation": "対向車の速度や距離は見誤りやすく、対向直進車には優先権があります。十分な余裕がないときは待ちます。", "category": "安全運転"},
    {"q": "二輪車は車体が小さいため、実際より遠くにいて、速度も遅いように見えることがある。", "answer": True, "explanation": "二輪車との距離や速度は錯覚しやすいため、右折時などは特に慎重に判断します。", "category": "安全運転"},
    {"q": "学校や住宅街の近くでも、歩行者が見えなければ通常の速度で走行してよい。", "answer": False, "explanation": "子供や高齢者は急な飛び出しをすることがあります。学校・住宅街では、いつでも止まれる速度と注意が必要です。", "category": "安全運転"},
    {"q": "長い下り坂でフットブレーキを使い続けると、ブレーキの効きが悪くなることがあるため、エンジンブレーキを活用する。", "answer": True, "explanation": "フットブレーキの多用はフェード現象を招きます。下り坂では低速ギアでエンジンブレーキを使います。", "category": "安全運転"},
    {"q": "ABS装備車が急ブレーキをかけるときは、ブレーキペダルを強く踏み続けるのが正しい操作である。", "answer": True, "explanation": "ABS装備車では、ペダルを強く踏み続けることでタイヤのロックを防ぎながら止まれます。ペダルへの反動を感じても踏み続けます。", "category": "安全運転"},
    {"q": "雪道や凍結した道路では、急発進・急ブレーキ・急ハンドルを避け、車間距離を長く取る。", "answer": True, "explanation": "滑りやすい路面では「急」のつく操作がスリップの原因になります。早めの減速と十分な車間距離が大切です。", "category": "安全運転"},
    {"q": "霧で見通しが悪いときは、前照灯やフォグランプを点灯し、速度を落として走行する。", "answer": True, "explanation": "霧のときは自車の存在を知らせる点灯と減速が基本です。中央線やガードレールも目安にします。", "category": "安全運転"},
    {"q": "強風のときは、速度を上げて早く通過した方がハンドルを取られず安全である。", "answer": False, "explanation": "強風時は速度を落とし、両手でハンドルをしっかり保持します。速度を上げると横風の影響が大きくなります。", "category": "安全運転"},
    {"q": "信号が青の横断歩道では歩行者は来ないので、左折・右折のとき歩行者に注意する必要はない。", "answer": False, "explanation": "青信号でも横断歩道には歩行者や自転車がいることがあります。右左折時は歩行者の有無を必ず確認します。", "category": "安全運転"},
    {"q": "進路変更をするときは、合図を出してから約3秒後に進路変更を始める。", "answer": True, "explanation": "合図は進路変更の3秒前、右左折・転回は30メートル手前が目安です。合図と同時に動くと周囲が対応できません。", "category": "安全運転"},
    {"q": "交差点で右折や左折をするときは、その交差点の30メートル手前の地点から合図を出す。", "answer": True, "explanation": "右左折・転回の合図は30メートル手前から出し、曲がり終わるまで継続します。", "category": "安全運転"},
    {"q": "進路変更の合図は、進路変更が終わった後に消せばよい。", "answer": False, "explanation": "合図は進路変更をしている間出し続け、終わったら速やかに消します。出しっぱなしも誤解を招きます。", "category": "安全運転"},
    {"q": "後ろから追い越しをかけられたときは、対抗して速度を上げてもよい。", "answer": False, "explanation": "追い越しをかけられた車両は、速度を上げたり進路をふさいだりして追い越しを妨げてはなりません。", "category": "安全運転"},
    {"q": "踏切を渡るときは、一時停止して左右の安全を確認し、低速ギアのまま一気に渡り切る。", "answer": True, "explanation": "踏切内でのギアチェンジはエンストのもとです。一時停止・安全確認のうえ、低速ギアで渡り切ります。", "category": "安全運転"},
# ---- 車両・応急・その他 ----
{"q": "交通事故を起こして人を死傷させたときは、直ちに車両を停止し、負傷者を救護するとともに、警察官に事故を報告しなければならない。", "answer": True, "explanation": "救護義務と報告義務は運転者の基本的な義務です。救護を怠って立ち去ると「ひき逃げ」として重く処罰されます。", "category": "車両・応急・その他"},
{"q": "軽い接触事故で、相手に怪我がないように見えるときは、その場を離れてもよい。", "answer": False, "explanation": "怪我の有無は見た目では判断できません。必ず停車して安全を確保し、相手の状態を確認して警察に報告します。", "category": "車両・応急・その他"},
{"q": "負傷者に出血がある場合は、清潔な布やガーゼを傷口に当てて強く圧迫し、止血に努める。", "answer": True, "explanation": "出血への基本対応は直接圧迫止血です。清潔な布で圧迫を続け、救急隊の到着を待ちます。", "category": "車両・応急・その他"},
{"q": "頭や首を強く打った疑いのある負傷者は、むやみに動かしてはならない。", "answer": True, "explanation": "頭部・頸部の損傷が疑われる場合は、動かすことで症状が悪化するおそれがあります。緊急時を除き、その場で救急隊を待ちます。", "category": "車両・応急・その他"},
{"q": "発炎筒は、昼間の見通しのよい場所でだけ使用する器具である。", "answer": False, "explanation": "発炎筒は、夜間やトンネル内、濃霧のときなどに自車の位置を後続車へ知らせるための器具です。昼夜を問わず使えます。", "category": "車両・応急・その他"},
{"q": "6歳未満の幼児を乗せて運転するときは、チャイルドシートを使用しなければならない。", "answer": True, "explanation": "幼児用補助装置（チャイルドシート）の使用は6歳未満の幼児が対象です。体格に合ったものを正しく取り付けます。", "category": "車両・応急・その他"},
{"q": "チャイルドシートの使用義務は、6歳以上12歳未満の子供にもある。", "answer": False, "explanation": "使用義務があるのは6歳未満の幼児です。ただし、6歳以上でも体格に合ったシートの使用が安全上望ましいとされています。", "category": "車両・応急・その他"},
{"q": "後部座席の同乗者にも、シートベルトの着用が義務付けられている。", "answer": True, "explanation": "シートベルトは全席で着用義務があります。運転者は同乗者にも着用させるよう努めなければなりません。", "category": "車両・応急・その他"},
{"q": "助手席の同乗者は、シートベルトを着用しなくてもよい。", "answer": False, "explanation": "助手席も着用義務の対象です。着用しない同乗者を乗せて運転すると、運転者が違反に問われることがあります。", "category": "車両・応急・その他"},
{"q": "自家用普通乗用自動車の車検（継続検査）の有効期間は、新車登録時の初回が3年、その後は2年ごとである。", "answer": True, "explanation": "自家用乗用車の車検は初回3年・以降2年ごとです。有効期間を過ぎた車両は公道を走行できません。", "category": "車両・応急・その他"},
{"q": "自賠責保険（自動車損害賠償責任保険）に加入していない自動車を運転してはならない。", "answer": True, "explanation": "自賠責保険は強制保険で、未加入車両の運行は処罰の対象です。保険証明書の携帯も義務付けられています。", "category": "車両・応急・その他"},
{"q": "自賠責保険の証明書は、自宅に保管しておけば、車両に備え付けなくてよい。", "answer": False, "explanation": "自賠責保険の証明書は、運転時に携帯（車両への備え付け）しなければなりません。", "category": "車両・応急・その他"},
{"q": "交通違反を繰り返して累積点数が一定の基準に達すると、免許の停止や取消しの処分を受ける。", "answer": True, "explanation": "点数制度では、過去の違反歴や累積点数に応じて停止・取消しなどの行政処分が行われます。", "category": "車両・応急・その他"},
{"q": "免許停止処分を受けた場合でも、停止処分者講習を受ければ累積点数はすべて消える。", "answer": False, "explanation": "講習を受けると停止期間が短縮されることはありますが、累積点数そのものが消えるわけではありません。", "category": "車両・応急・その他"},
{"q": "自動車を運転するときは、運転免許証を携帯しなければならない。", "answer": True, "explanation": "免許証の携帯は義務です。不携帯は違反となり、警察官から提示を求められたときは提示しなければなりません。", "category": "車両・応急・その他"},
{"q": "積載物の長さは、原則として車両の長さの1.1倍（10分の11）を超えてはならない。", "answer": True, "explanation": "積載の制限は、長さ＝車両の長さの1.1倍まで、幅＝車両の幅まで、高さ＝地上3.8メートルまでが原則です。", "category": "車両・応急・その他"},
{"q": "積載物の高さは、原則として地上から4.5メートルまで認められている。", "answer": False, "explanation": "積載物の高さの制限は地上3.8メートルまでです（高さが指定された道路などで4.1メートルまで認められる場合を除きます）。", "category": "車両・応急・その他"},
{"q": "12歳未満の子供は、乗車定員を計算するとき人数に含めない。", "answer": False, "explanation": "12歳未満の子供は、3人を大人2人分として数えます。人数に含めないわけではありません。", "category": "車両・応急・その他"},
{"q": "タイヤの溝の深さが1.6ミリメートル以下になりスリップサインが出たタイヤは、使用してはならない。", "answer": True, "explanation": "スリップサインが現れたタイヤは整備不良となり使用できません。雨天時の制動距離も大きく延びます。", "category": "車両・応急・その他"},
{"q": "故障車をロープでけん引するときは、ロープの長さを5メートル以内にし、0.3メートル四方以上の白い布をロープに結び付ける。", "answer": True, "explanation": "けん引の決まりです。けん引される車両との間隔を保ち、後続車からロープが見えるようにします。", "category": "車両・応急・その他"},
{"q": "故障車のけん引は、車両の重さにかかわらず、普通免許だけあれば誰でもできる。", "answer": False, "explanation": "車両総重量が750キログラムを超える故障車をけん引するには、けん引免許が必要です。", "category": "車両・応急・その他"},
{"q": "自動二輪車に乗るときは、運転者だけでなく同乗者も乗車用ヘルメットをかぶらなければならない。", "answer": True, "explanation": "二輪車のヘルメット着用は運転者・同乗者の双方に義務があります。あごひもを確実に締めることが大切です。", "category": "車両・応急・その他"},
{"q": "原動機付自転車は、交差点で右折するとき、原則として二段階右折をしなければならない。", "answer": True, "explanation": "原付の右折は二段階右折が原則です。ただし、二段階右折が禁止されている交差点では通常の方法で右折します。", "category": "車両・応急・その他"},
{"q": "交差点とその側端から5メートル以内の場所では、停車はできるが駐車はできない。", "answer": False, "explanation": "交差点とその側端から5メートル以内は、駐車も停車も禁止されている場所です。", "category": "車両・応急・その他"},
]

CATEGORIES = ["法規の基礎", "標識・標示", "高速道路", "安全運転", "車両・応急・その他"]

# ============================================================
# Unit 2: Web アプリ
# ============================================================
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>本免対策 ○×カード</title>
<style>
* { box-sizing: border-box;}
html, body { margin: 0; padding: 0; overflow-x: hidden;}
body {
font-family: -apple-system, "Hiragino Sans", "Noto Sans JP", sans-serif;
background: var(--bg); color: var(--fg);
--bg: #f4f6f8; --fg: #1c2430; --card: #ffffff; --line: #d5dce4;
--accent: #2563eb; --ok: #15803d; --ng: #dc2626;
}
body[data-theme="dark"] {
--bg: #12161d; --fg: #e6ebf2; --card: #1d242f; --line: #39445a;
--accent: #60a5fa; --ok: #4ade80; --ng: #f87171;
}
.wrap { max-width: 640px; margin: 0 auto; padding: 16px;}
header { display: flex; justify-content: space-between; align-items: center; gap: 8px;}
h1 { font-size: 1.35rem; margin: 8px 0;}
.theme-btn { border: 1px solid var(--line); background: var(--card); color: var(--fg);
border-radius: 8px; padding: 6px 12px; cursor: pointer; white-space: nowrap;}
.card { background: var(--card); border: 1px solid var(--line); border-radius: 14px;
padding: 20px; margin-top: 14px;}
.disclaimer { font-size: 0.85rem; line-height: 1.6; opacity: 0.85;}
.mode-btn,.cat-btn { display: block; width: 100%; margin: 10px 0; padding: 14px;
font-size: 1.05rem; border-radius: 10px; border: 1px solid var(--line);
background: var(--card); color: var(--fg); cursor: pointer;}
.mode-btn.primary { background: var(--accent); color: #fff; border-color: var(--accent);}
.meta { display: flex; justify-content: space-between; font-size: 0.9rem; opacity: 0.85;}
.qtext { font-size: 1.15rem; line-height: 1.8; margin: 14px 0 20px; overflow-wrap: break-word;}
.ox-row { display: flex; gap: 14px;}
.ox-btn { flex: 1; font-size: 2.6rem; padding: 18px 0; border-radius: 14px; cursor: pointer;
border: 2px solid var(--line); background: var(--card); color: var(--fg);}
.ox-btn:disabled { opacity: 0.55; cursor: default;}
.feedback { margin-top: 16px; font-size: 1rem; line-height: 1.7; display: none;}
.feedback.verdict { font-weight: bold; font-size: 1.2rem;}
.ok { color: var(--ok);}.ng { color: var(--ng);}
.next-btn { display: none; width: 100%; margin-top: 14px; padding: 13px; font-size: 1.05rem;
border-radius: 10px; border: none; background: var(--accent); color: #fff; cursor: pointer;}
.missed-item { border-top: 1px solid var(--line); padding: 10px 0; font-size: 0.95rem; line-height: 1.6;}
.score-big { font-size: 2rem; font-weight: bold; text-align: center; margin: 10px 0;}
.center { text-align: center;}
[hidden] { display: none!important;}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>本免対策 ○×カード</h1>
<button class="theme-btn" id="themeBtn" type="button">🌙 ダーク</button>
</header>

<section id="homeView">
<div class="card">
<p class="disclaimer">学習用の自作問題です。公式の試験問題ではありません。本免学科試験のイラスト問題（危険予測）は含みません。</p>
<button class="mode-btn primary" id="btnRandom" type="button">ランダム10問</button>
<button class="mode-btn" id="btnAll" type="button">全問120問</button>
<p style="margin:16px 0 4px;">カテゴリ別（各24問）</p>
<div id="catButtons"></div>
<button class="mode-btn" id="btnReview" type="button" hidden>間違えた問題だけ復習（<span id="missedCount">0</span>問）</button>
</div>
</section>

<section id="quizView" hidden>
<div class="card">
<div class="meta"><span id="progress"></span><span id="scoreNow"></span></div>
<div class="meta"><span id="catLabel"></span><span></span></div>
<p class="qtext" id="qText"></p>
<div class="ox-row">
<button class="ox-btn" id="btnMaru" type="button">○</button>
<button class="ox-btn" id="btnBatsu" type="button">×</button>
</div>
<div class="feedback" id="feedback">
<div class="verdict" id="verdict"></div>
<div id="explanation"></div>
</div>
<button class="next-btn" id="btnNext" type="button">次の問題</button>
</div>
</section>

<section id="resultView" hidden>
<div class="card">
<div class="score-big" id="scoreBig"></div>
<p class="center" id="passLine"></p>
<div id="missedList"></div>
<button class="mode-btn primary" id="btnReview2" type="button" hidden>間違えた問題だけ復習</button>
<button class="mode-btn" id="btnHome" type="button">トップに戻る</button>
</div>
</section>
</div>

<script>
const QUESTIONS = {{ questions | tojson}};
const CATEGORIES = {{ categories | tojson}};
const MISSED_KEY = "honmenquiz_missed";
const THEME_KEY = "honmenquiz_theme";

let deck = [], idx = 0, score = 0, missed = [], answered = false;

function shuffle(a) {
for (let i = a.length - 1; i > 0; i--) {
const j = Math.floor(Math.random() * (i + 1));
[a[i], a[j]] = [a[j], a[i]];
}
return a;
}
function loadMissed() {
try { return JSON.parse(localStorage.getItem(MISSED_KEY) || "[]");}
catch (e) { return [];}
}
function saveMissed(list) {
localStorage.setItem(MISSED_KEY, JSON.stringify(list));
}
function show(view) {
for (const id of ["homeView", "quizView", "resultView"]) {
document.getElementById(id).hidden = (id!== view);
}
if (view === "homeView") refreshReviewBtn();
}
function refreshReviewBtn() {
const n = loadMissed().length;
document.getElementById("missedCount").textContent = n;
document.getElementById("btnReview").hidden = (n === 0);
}
function startQuiz(questions) {
deck = questions.slice(); idx = 0; score = 0; missed = []; answered = false;
show("quizView"); renderQuestion();
}
function renderQuestion() {
const q = deck[idx];
document.getElementById("progress").textContent = (idx + 1) + " / " + deck.length;
document.getElementById("scoreNow").textContent = "正解 " + score;
document.getElementById("catLabel").textContent = q.category;
document.getElementById("qText").textContent = q.q;
document.getElementById("feedback").style.display = "none";
document.getElementById("btnNext").style.display = "none";
document.getElementById("btnMaru").disabled = false;
document.getElementById("btnBatsu").disabled = false;
answered = false;
}
function answer(userSaysTrue) {
if (answered) return;
answered = true;
const q = deck[idx];
const correct = (userSaysTrue === q.answer);
const verdict = document.getElementById("verdict");
if (correct) {
score++;
verdict.textContent = "正解！ 答えは " + (q.answer? "○": "×");
verdict.className = "verdict ok";
} else {
verdict.textContent = "不正解… 答えは " + (q.answer? "○": "×");
verdict.className = "verdict ng";
missed.push(q);
}
document.getElementById("scoreNow").textContent = "正解 " + score;
document.getElementById("explanation").textContent = q.explanation;
document.getElementById("feedback").style.display = "block";
document.getElementById("btnMaru").disabled = true;
document.getElementById("btnBatsu").disabled = true;
const next = document.getElementById("btnNext");
next.textContent = (idx + 1 < deck.length)? "次の問題": "結果を見る";
next.style.display = "block";
}
function finish() {
// 今回のミスを保存済みリストへマージ（問題文で重複排除）
const stored = loadMissed();
const seen = new Set(stored.map(x => x.q));
for (const m of missed) if (!seen.has(m.q)) { stored.push(m); seen.add(m.q);}
saveMissed(stored);
const total = deck.length;
const pct = total? Math.round(score / total * 100): 0;
document.getElementById("scoreBig").textContent = score + " / " + total + " 点（" + pct + "%）";
document.getElementById("passLine").textContent =
"本免学科の合格ライン目安は90%です。" + (pct >= 90? " 合格ライン達成！": " あと少し、復習しよう。");
const list = document.getElementById("missedList");
list.innerHTML = "";
if (missed.length) {
const h = document.createElement("p");
h.textContent = "間違えた問題（" + missed.length + "問）";
list.appendChild(h);
for (const m of missed) {
const d = document.createElement("div");
d.className = "missed-item";
d.textContent = "" + m.q + "（答え：" + (m.answer? "○": "×") + "） " + m.explanation;
list.appendChild(d);
}
} else {
list.innerHTML = "<p class='center'>全問正解！</p>";
}
document.getElementById("btnReview2").hidden = (loadMissed().length === 0);
show("resultView");
}

document.getElementById("btnRandom").onclick = () => startQuiz(shuffle(QUESTIONS.slice()).slice(0, 10));
document.getElementById("btnAll").onclick = () => startQuiz(shuffle(QUESTIONS.slice()));
document.getElementById("btnReview").onclick = () => startQuiz(shuffle(loadMissed()));
document.getElementById("btnReview2").onclick = () => startQuiz(shuffle(loadMissed()));
document.getElementById("btnHome").onclick = () => show("homeView");
document.getElementById("btnMaru").onclick = () => answer(true);
document.getElementById("btnBatsu").onclick = () => answer(false);
document.getElementById("btnNext").onclick = () => {
idx++;
if (idx < deck.length) renderQuestion(); else finish();
};

const catBox = document.getElementById("catButtons");
for (const c of CATEGORIES) {
const b = document.createElement("button");
b.className = "cat-btn"; b.type = "button"; b.textContent = c;
b.onclick = () => startQuiz(shuffle(QUESTIONS.filter(q => q.category === c)));
catBox.appendChild(b);
}

// テーマ（ライト/ダーク）
const themeBtn = document.getElementById("themeBtn");
function applyTheme(t) {
document.body.dataset.theme = t;
themeBtn.textContent = (t === "dark")? "☀️ ライト": "🌙 ダーク";
}
applyTheme(localStorage.getItem(THEME_KEY) || "light");
themeBtn.onclick = () => {
const next = (document.body.dataset.theme === "dark")? "light": "dark";
localStorage.setItem(THEME_KEY, next);
applyTheme(next);
};
refreshReviewBtn();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML, questions=QUESTIONS, categories=CATEGORIES)


@app.route("/api/questions")
def api_questions():
    return jsonify(QUESTIONS)


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
