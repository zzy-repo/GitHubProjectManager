# GitHub Repos Fetcher 使用文档 🚀

## 简介 📝
`GitHub Repos Fetcher` 是一个基于 PyQt5 的桌面应用程序，允许用户通过提供 GitHub 个人访问 Token 来获取其所有仓库的信息，并能选择性地删除仓库。

## 功能 🔧
1. **获取 GitHub 仓库**: 通过 GitHub 个人访问 Token 获取用户的仓库信息，并在表格中显示仓库名称及描述。 📂
2. **删除选中仓库**: 用户可选择表格中的仓库，点击删除按钮进行删除。 🗑️
3. **帮助获取 Token**: 提供获取 GitHub Token 的指导信息。 💡

## 使用方法 💻

### 1. 启动应用 🎬
运行程序后，应用窗口会显示输入框和按钮。

### 2. 获取仓库信息 🔍
1. 输入你的 **GitHub 用户名**（可选）和 **GitHub Token**。
   - 你可以在 [GitHub Token 页面](https://github.com/settings/tokens) 获取你的 Token，确保拥有 `repo` 权限。
2. 点击 **Fetch Repositories** 按钮。 🏃‍♂️
   - 如果 Token 有效，应用会获取并显示你的仓库列表。

### 3. 删除仓库 🗑️
1. 在仓库列表中，勾选你希望删除的仓库旁边的复选框。 ✔️
2. 点击 **Delete Selected Repositories** 按钮。 🚨
3. 系统会提示你确认是否删除选中的仓库。确认后，所选仓库将被删除。

### 4. 获取 GitHub Token 帮助 ❓
点击 **How to Get Token** 按钮，系统会显示如何获取 GitHub 个人访问 Token 的步骤。 🛠️

## 注意事项 ⚠️
- **Token 必须具有 `repo` 权限**，否则无法获取私有仓库或删除仓库。 🔑
- 删除操作不可逆，请小心使用。 ⚰️

## 技术实现 🧑‍💻
- **PyQt5**: 用于创建桌面界面。 🖥️
- **GitHub API**: 用于获取仓库信息和删除仓库。 🌐
