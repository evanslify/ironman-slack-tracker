# 催文機

協助你完成 [iT邦幫忙鐵人賽](https://ithelp.ithome.com.tw/ironman/signup/team/46)。

# 用途

此 Bot 設計是在 Lambda 上執行，並呼叫 Slack Webhook API 來標註在執行時還沒發文的人。

# 使用方法

1. 在 `team_member.py` 中寫入你的隊伍成員資訊。

```python
team_members = [
    {'slack_handle': '<slack id>', 'iron_man_id': '<iron id>'}
]
```

`iron id` 爲鐵人賽主題 ID。例如 `https://ithelp.ithome.com.tw/users/20107704/ironman/1953` 中，ID 爲 1953。
`slack id` 爲 Slack 內部 ID。觀看使用者的個人檔案中，選單中有一 "Copy Member ID"。

2. L13 的 URL 需要改成你的團隊首頁。把 `50` 改成你的團隊 ID。

# 部屬

此專案使用 `python-lambda` 來部屬。
