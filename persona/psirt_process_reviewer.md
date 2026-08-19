# PSIRT Process Reviewer Persona

> ⚠️ **本檔非權威來源，請勿在此編輯（pointer stub）。**
>
> **權威來源（Single Source of Truth）**：`hanuman` 專案的
> `.claude/agents/psirt_process_reviewer.md`
> —— 該定義已於 2026-08-19 擴寫為可派工的 subagent（含 frontmatter、七個審查構面、
> 四段回傳格式），本檔原為 2026-05 的 12 行舊版。
>
> 兩份並存必然漂移，且漂移不會有任何工具報錯——與本 repo `doc/L2-01_…` 在 hanuman 側
> 採指標樁的理由相同：**保留檔名／路徑供既有引用解析，實際內容一律以權威來源為準**。
>
> **取得權威內容：**
> - 本機開發佈局（corepoint / clotho / hanuman 同層）相對路徑：
>   `../../hanuman/.claude/agents/psirt_process_reviewer.md`
> - 或於 hanuman repo 內：`.claude/agents/psirt_process_reviewer.md`
>
> **在 corepoint 內怎麼用：** 那是 hanuman **專案層**的 subagent，在 corepoint 開的
> session 裡叫不到它。要用時讀取該檔內容，當作角色定義寫進 prompt 即可——corepoint 的
> `persona/` 本來就是「prompting 時使用的角色定義」。若日後希望兩個 repo 都能直接派工，
> 應將該定義提升到使用者層 `~/.claude/agents/`，而不是在此複製一份。
>
> **審查 L2-01 時的重要前提：** 權威來源是本 repo 的
> `doc/L2-01_vulnerability-handling-and-disclosure-process.md`（§1–§8 完整程序），
> **不是** hanuman 的 `ref/L2-01_…`（那一份也是指標樁）。
>
> 本檔歷史（原 persona 內容）見 git 歷史。
