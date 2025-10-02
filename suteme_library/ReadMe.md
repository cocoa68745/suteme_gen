## Suteme
https://m.kuku.lu/ というステメアドを作れるサイトを操作するライブラリ
```pip install requests beautifulsoup4```

## 使い方
```python
suteme = Suteme()
# tokenを確認
suteme.check_token()
# メール作る
first_mail = suteme.add_mail()
# 30日間有効なメール発行
onetime_mail = suteme.add_onetime_mail()

# 今あるメール一覧
print(suteme.get_all_mail)

# 最新のメールの中身取得
print(suteme.get_top_mail(first_mail))
```

使い方わからなければプロフのディスコードまで。
アカウント作るときに必要な認証コード自動で取得する機能も付ける予定です。
ちなみにログインするときは  
`suteme = Suteme(csrf_token, sessionhash)`