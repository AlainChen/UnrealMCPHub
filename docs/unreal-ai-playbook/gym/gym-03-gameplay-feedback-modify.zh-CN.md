# Gym-03 Gameplay Feedback Modify

## Status

- `Domain`: `3d-gameplay-feedback`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `planned`

## Goal

鍦ㄤ竴涓交閲忋€佸彲鎺у埗鐨?3D 鍦烘櫙涓婏紝鑷姩瀹屾垚涓€娆℃渶灏忕殑 `gameplay feedback` 淇敼锛屽苟鐣欎笅鍙綊妗ｇ殑 before/after 璇佹嵁銆?

`Gym-03` 涓嶆槸瀹屾暣 gameplay loop 閲嶅仛锛屼篃涓嶆槸澶у瀷 systems benchmark銆?

瀹冪殑鐩爣鏄獙璇侊細
- AI 鑳藉惁瀵逛竴涓凡鏈夌殑 3D 浜や簰鎴栬Е鍙戞儏鏅紝鍋氬嚭鏄庣‘鍙鐨勫弽棣?
- 褰撳墠 workflow 鏄惁鑳芥壙鎺?feedback 绫?modify 浠诲姟
- 钃濆浘閫昏緫鏄惁鍙互浣滀负杩欎竴鍩熺殑鎺ㄨ崘楠岃瘉璺緞

## Recommended Scenario

`Gym-03` 鏈€閫傚悎鐨勪笉鏄噸 combat锛岃€屾槸杞婚噺浜や簰涓庡弽棣堟儏鏅€?

鎺ㄨ崘 baseline scenario锛?
- overlap trigger
- click / interact trigger
- simple proximity event
- one-shot state change with visible response

渚嬪锛?
- 鐜╁鎴栨憚鍍忔満杩涘叆 trigger 鍖哄煙鍚庯紝瀵硅薄棰滆壊銆佹潗璐ㄦ垨 scale 鍙戠敓鍙樺寲
- 瑙﹀彂鍚庡嚭鐜颁竴涓畝鍗曟彁绀恒€佺伅鍏夊彉鍖栨垨璺熼殢鍙嶉
- 瑙﹀彂鍚庝竴涓洰鏍囧彉鎴愨€滆婵€娲绘垨琚壘鍒扳€濈姸鎬?

## Recommended Implementation Path

褰撳墠鎺ㄨ崘涓ょ baseline 璺緞锛?

### Path A: Actor / Scene Feedback

鐩存帴鍩轰簬宸叉湁 Actor 鍜屽満鏅伐鍏峰仛鍙嶉淇敼锛?
- transform
- visibility
- light
- supporting prop response

杩欐潯璺緞鏇撮€傚悎鍏堣窇閫氭渶灏?feedback chain銆?

### Path B: Blueprint Logic Modify

钃濆浘閫昏緫淇敼搴斾綔涓?`Gym-03` 鐨勬帹鑽愰獙璇佽矾寰勶紝鑰屼笉鏄崟鐙殑 Gym 缂栧彿銆?

鎺ㄨ崘鐢ㄤ簬锛?
- overlap event
- simple trigger logic
- timer-driven feedback
- Widget / prompt glue logic

杩欒兘鏇村ソ鍦伴獙璇侊細
- AI 鏄惁鐪熸鐞嗚В Unreal 钃濆浘鐨勫眬閮ㄤ慨鏀?
- AI 鏄惁鑳藉湪涓嶅ぇ骞呴噸鏋勯€昏緫鐨勬儏鍐典笅鍋氬嚭鏈夋剰涔夌殑鍙嶉鏀瑰姩

## Scope

鍏佽淇敼锛?
- overlap / trigger 鍙嶉
- 鐗╀欢棰滆壊銆佹潗璐ㄣ€乻cale銆乿isibility 鍙樺寲
- 灏忚寖鍥村睍绀虹伅鍏夋垨 UI 鎻愮ず
- 灏戦噺 Blueprint event / component / variable 淇敼

鏈疆涓嶅仛锛?
- 澶у瀷 combat loop
- 澶嶆潅 AI 行为
- 閲嶅瀷 animation state machine
- 澶ц寖鍥?UI 閲嶆瀯

## Relationship To Earlier Gyms

- `Gym-01` 鍋忓悜锛?focal readability and lighting
- `Gym-02` 鍋忓悜锛?spatial readability and local hierarchy
- `Gym-03` 鍋忓悜锛?interactive readability and player-facing response

鎹㈠彞璇濊锛?
`Gym-03` 鎶?鈥滆兘鐪嬫噦鈥濇洿杩戜竴姝ュ彉鎴?鈥滆兘鎰熷彈鍒扳€濄€?

## Recommended Tool Path

浼樺厛渚濊禆宸茬粡鍦?`RemoteMCP` 渚ч獙璇佽繃鐨勮兘鍔涳細

- scene/testbed construction
- evidence capture
- health / reconnect baseline
- lighting baseline for readability support

褰撳墠濡傛灉瑕佽蛋 Blueprint validation锛岄渶瑕侀噸鐢ㄧ幇鏈夌殑 blueprint domain 能力锛屼絾 baseline 涓嶅簲璁捐鎴愰噸鍨?blueprint graph reconstruction銆?

## Baseline Pass

鏈疆 baseline 榛樿鍙仛涓や釜鍔ㄤ綔锛?

### Modify A: Trigger Feedback Pass

涓€涓?trigger / overlap / proximity 鏉′欢鍙戠敓鍚庯紝鐢熸垚涓€涓槑鏄剧殑鍙嶉銆?

### Modify B: Readability Support Pass

涓哄弽棣堝鍔犱竴鐐逛紶杈惧姏锛屼緥濡傦細
- supporting light
- scale punch
- simple prompt
- one-shot highlight

## Evidence Bundle

鏈€灏忚瘉鎹寘鍥哄畾涓猴細

- task brief
- before image
- after image or paired state image
- execution summary
- interaction / feedback note
- risk note
- readiness conclusion

濡傛灉鍚敤浜?Blueprint path锛岃瘉鎹腑杩樺簲琛ュ厖锛?
- modified blueprint name
- modified event or logic area
- whether the change remained local or expanded beyond baseline scope

## Success Criteria

鏈疆瀹屾垚鐨勬渶浣庢爣鍑嗭細

1. 鏈変竴涓槑纭殑 trigger / feedback 鎯呮櫙
2. 鏈変竴缁勫彲瑙嗗寲鍓嶅悗瀵规瘮
3. feedback 鏈夋竻鏅扮殑鐜╁鎰熺煡浠峰€?
4. 濡傛灉浣跨敤 Blueprint path锛屼慨鏀归渶淇濇寔灞€閮ㄣ€佸彲瑙ｉ噴銆佸彲鍥炴斁

## Hand-Off

瀹屾垚鍚庡簲鍥炲～锛?

- 缁撴灉鎽樿
- 璇佹嵁鏂囦欢鍚?
- 椋庨櫓缁撹
- 鏄惁鏇撮€傚悎缁х画鐢?Actor path 杩樻槸 Blueprint path
- 鏄惁鍑嗗杩涘叆 `Gym-04`
