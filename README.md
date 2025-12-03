# DiabloIV_Blood_Bone_Restorer — CI Windows EXE Build

说明：本仓库已添加 GitHub Actions workflow 用于在 `windows-latest` runner 上构建单文件 Windows EXE（通过 PyInstaller）。构建结果会作为 artifact 上传；当你推送以 `v*` 为前缀的 tag（例如 `v1.0.0`）时，workflow 会把 exe 附加为 GitHub Release 资产。

快速使用说明：

- 本地构建（在 Windows PowerShell）：

```powershell
.\build_windows.ps1 -Name "DiabloIV_BBR"
```

- 在 GitHub 上触发：
  - Push 到 `main` 会触发构建并上传 artifact（但不会自动创建 Release，除非你 push tag）。
  - Push 一个 tag，如 `git tag v1.0.0 && git push origin v1.0.0` 会触发构建并把 exe 附加到 Release。

产物位置：`dist/DiabloIV_BBR.exe`（在 workflow 中上传为 artifact）。

注意事项：
- 单文件 exe 可能较大，且部分杀毒软件会误报。建议在 Release 中提供 SHA256 校验和并说明签名状态。
- 如果需要代码签名（Authenticode），请准备证书并把签名步骤加入 CI；需要将证书凭据安全地放入 `secrets`。

如果你希望我继续：
- 我可以添加一个 PyInstaller spec 文件来更稳健地收集 Qt 插件与资源（建议）。
- 我可以把 workflow 改为在每次 `push` 到 `main` 自动创建/更新 Draft Release（如果你想要更自动化）。
