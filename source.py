import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class GitHubRepoFetcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub Repos Fetcher")
        self.setGeometry(100, 100, 800, 600)

        # 设置字体
        self.set_font()

        # 设置窗口样式
        self.set_styles()

        # 创建 UI 元素
        self.init_ui()

        # 用于保存仓库信息
        self.repos = []

    def set_font(self):
        """设置窗口字体"""
        font = QFont("Arial", 12)
        self.setFont(font)

    def set_styles(self):
        """设置窗口背景色和按钮样式"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
            }
            QLabel {
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

    def init_ui(self):
        """初始化 UI 组件"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # 设置外边距
        layout.setSpacing(20)  # 设置间距

        # 用户名和Token输入框
        self.username_label = QLabel("GitHub Username (optional):")
        self.username_input = QLineEdit()

        self.token_label = QLabel("Enter GitHub Personal Access Token:")
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)  # 隐藏Token输入

        self.fetch_button = QPushButton("Fetch Repositories")
        self.delete_button = QPushButton("Delete Selected Repositories")
        self.help_button = QPushButton("How to Get Token")  # 新增帮助按钮

        # 设置按钮点击事件
        self.fetch_button.clicked.connect(self.fetch_repos)
        self.delete_button.clicked.connect(self.delete_selected_repos)
        self.help_button.clicked.connect(self.show_help)  # 帮助按钮点击事件

        # 表格设置
        self.repo_table = QTableWidget()
        self.repo_table.setColumnCount(3)
        self.repo_table.setHorizontalHeaderLabels(["Select", "Name", "Description"])
        self.repo_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选择整行
        header = self.repo_table.horizontalHeader()
        # 设置第一列（复选框列）宽度固定，不允许调整
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.repo_table.setColumnWidth(0, 30)
        # 设置第二列（仓库名称列）宽度自适应，自动调整
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.repo_table.setColumnWidth(0, 100)
        # 设置第三列（描述列）宽度自动调整
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # 布局组合
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_input)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.repo_table)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.help_button)  # 将帮助按钮添加到布局中

        # 设置主布局
        self.setLayout(layout)

    def fetch_repos(self):
        """获取仓库信息"""
        token = self.token_input.text().strip()

        if not token:
            QMessageBox.warning(self, "Input Error", "Please provide a GitHub token.")
            return

        # 使用 Token 获取当前用户信息
        user_url = "https://api.github.com/user"
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.get(user_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data['login']  # 获取当前用户名
            self.username_input.setText(username)  # 自动填充用户名输入框
            self.fetch_repos_by_user(username, token)  # 使用获取的用户名调用 fetch_repos_by_user
        else:
            QMessageBox.warning(self, "Error", f"Failed to fetch user info. HTTP Status: {response.status_code}")
            return

    def fetch_repos_by_user(self, username, token):
        """使用 GitHub 用户名获取仓库信息"""
        url = f"https://api.github.com/users/{username}/repos?per_page=100"
        headers = {
            'Authorization': f'token {token}',  # 使用用户输入的 GitHub Token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.repos = response.json()  # 保存仓库信息
            self.display_repos(self.repos)
        else:
            self.repo_table.setRowCount(0)  # 清空表格内容
            self.repo_table.setRowCount(1)
            self.repo_table.setItem(0, 0, QTableWidgetItem(
                f"Error fetching repositories. HTTP Status: {response.status_code}"))

    def display_repos(self, repos):
        """将仓库信息显示到表格中"""
        self.repo_table.setRowCount(0)  # 清空表格
        for repo in repos:
            row_position = self.repo_table.rowCount()
            self.repo_table.insertRow(row_position)

            # 添加复选框
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.repo_table.setItem(row_position, 0, checkbox_item)

            # 添加仓库名称
            self.repo_table.setItem(row_position, 1, QTableWidgetItem(repo['name']))

            # 添加仓库描述，处理没有描述的情况
            description = repo['description'] if repo['description'] else 'No description available'
            self.repo_table.setItem(row_position, 2, QTableWidgetItem(description))

    def delete_selected_repos(self):
        """删除选中的仓库"""
        rows_to_delete = []

        # 获取Token
        token = self.token_input.text().strip()

        if not token:
            QMessageBox.warning(self, "Input Error", "Please provide a GitHub token.")
            return

        # 使用 Token 获取当前用户信息
        user_url = "https://api.github.com/user"
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.get(user_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data['login']  # 获取当前用户名
        else:
            QMessageBox.warning(self, "Error", f"Failed to fetch user info. HTTP Status: {response.status_code}")
            return

        # 遍历所有行，检查复选框是否被选中
        for row in range(self.repo_table.rowCount()):
            checkbox_item = self.repo_table.item(row, 0)
            if checkbox_item.checkState() == Qt.Checked:
                rows_to_delete.append(row)

        # 如果没有选中任何仓库，提示用户
        if not rows_to_delete:
            QMessageBox.warning(self, "No Selection", "Please select at least one repository to delete.")
            return

        # 确认删除
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            "Are you sure you want to delete the selected repositories?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.No:
            return

        # 删除选中的行并进行 GitHub API 删除
        for row in reversed(rows_to_delete):  # 从后往前删除，避免索引混乱
            repo_name = self.repo_table.item(row, 1).text()
            # 调用删除仓库的API
            self.delete_repo(username, repo_name, token)
            self.repo_table.removeRow(row)

        # 更新仓库信息，移除已删除的仓库
        self.repos = [repo for i, repo in enumerate(self.repos) if i not in rows_to_delete]

    def delete_repo(self, username, repo_name, token):
        """删除指定的仓库"""
        url = f"https://api.github.com/repos/{username}/{repo_name}"
        headers = {
            'Authorization': f'token {token}',  # 需要在这里使用用户输入的Token
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Repository {repo_name} deleted successfully.")
        else:
            print(f"Failed to delete repository {repo_name}. Status code: {response.status_code}")
            QMessageBox.critical(self, "Error", f"Failed to delete {repo_name}. Please try again.")

    def show_help(self):
        """显示如何获取 Token 的帮助信息"""
        help_message = (
            "To get your GitHub Personal Access Token:\n"
            "1. Go to https://github.com/settings/tokens\n"
            "2. Click 'Generate new token'.\n"
            "3. Select the scopes (permissions) you need.\n"
            "4. Click 'Generate token'.\n"
            "5. Copy the token and paste it here."
        )
        QMessageBox.information(self, "How to Get GitHub Token", help_message)


def main():
    app = QApplication(sys.argv)
    window = GitHubRepoFetcher()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
