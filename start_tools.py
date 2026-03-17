"""
Writer Tool 外置工具启动器（增强版）

提供统一的图形界面入口，可启动：
- 资源管理器 / 助手配置编辑器 / 事件分析工具
- 环境体检 / 工作区清理 / 发布包打包

双击此文件或运行 python start_tools.py 启动。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("错误: 未找到 tkinter 模块")
    sys.exit(1)


class ToolsLauncher(tk.Tk):
    """Unified tools launcher with modern UI."""

    TOOLS = [
        {
            "name": "资源管理器",
            "desc": "管理项目资源、编辑事件\n支持 .writerproj 项目文件",
            "script": "start_asset_editor.py",
            "icon": "📦",
            "color": "#4A90D9",
        },
        {
            "name": "助手配置编辑器",
            "desc": "配置浮动助手的事件和行为\nJSON 语法高亮编辑",
            "script": "start_assistant_event_editor.py",
            "icon": "⚙️",
            "color": "#7B68EE",
        },
        {
            "name": "事件分析工具",
            "desc": "分析事件逻辑、检测问题\n循环检测、死路径检测",
            "script": "analyze_events.py",
            "args": ["--gui"],
            "icon": "🔍",
            "color": "#2E7D32",
        },
        {
            "name": "环境体检",
            "desc": "检查 tkinter、核心依赖和关键文件\n适合覆盖升级后先跑一遍",
            "script": "scripts/maintenance/healthcheck.py",
            "args": ["--gui"],
            "icon": "🩺",
            "color": "#D35400",
        },
        {
            "name": "清理工作区",
            "desc": "删除 __pycache__、tmpclaude-*、dist\n清掉临时目录再打包",
            "script": "scripts/maintenance/cleanup_workspace.py",
            "args": ["--gui"],
            "icon": "🧹",
            "color": "#16A085",
        },
        {
            "name": "打包发布 ZIP",
            "desc": "自动排除缓存和临时目录\n生成干净的发布压缩包",
            "script": "scripts/release/build_release_zip.py",
            "args": ["--gui"],
            "icon": "🗜️",
            "color": "#C0392B",
        },
    ]

    def __init__(self):
        super().__init__()
        self.title("Writer Tool - 工具箱")
        self.geometry("620x700")
        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() - 620) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"+{x}+{y}")

        self.script_dir = Path(__file__).resolve().parent
        self._setup_ui()

    def _setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=88)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text="Writer Tool 工具箱",
            font=("Microsoft YaHei UI", 18, "bold"),
            fg="white",
            bg="#2C3E50",
        )
        title_label.pack(pady=(18, 0))

        sub_label = tk.Label(
            header,
            text="创作工具 + 维护脚本 + 打包发布",
            font=("Microsoft YaHei UI", 10),
            fg="#D7E3F0",
            bg="#2C3E50",
        )
        sub_label.pack(pady=(4, 0))

        container = tk.Frame(self, bg="#F5F5F5")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        for tool in self.TOOLS:
            self._create_tool_card(container, tool)

        footer = tk.Frame(self, bg="#F5F5F5")
        footer.pack(fill=tk.X, padx=20, pady=(0, 15))

        version_label = tk.Label(
            footer,
            text="Writer Tool v1.10 | 工程增强工具箱",
            font=("Microsoft YaHei UI", 9),
            fg="#888888",
            bg="#F5F5F5",
        )
        version_label.pack(side=tk.LEFT)

        help_btn = tk.Button(
            footer,
            text="帮助",
            font=("Microsoft YaHei UI", 9),
            relief=tk.FLAT,
            bg="#F5F5F5",
            fg="#666666",
            cursor="hand2",
            command=self._show_help,
        )
        help_btn.pack(side=tk.RIGHT)

    def _create_tool_card(self, parent, tool: dict):
        card = tk.Frame(
            parent,
            bg="white",
            relief=tk.FLAT,
            highlightbackground="#E0E0E0",
            highlightthickness=1,
        )
        card.pack(fill=tk.X, pady=7)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill=tk.X, padx=15, pady=12)

        icon_label = tk.Label(
            inner,
            text=tool["icon"],
            font=("Segoe UI Emoji", 24),
            bg="white",
        )
        icon_label.pack(side=tk.LEFT)

        text_frame = tk.Frame(inner, bg="white")
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)

        name_label = tk.Label(
            text_frame,
            text=tool["name"],
            font=("Microsoft YaHei UI", 12, "bold"),
            fg="#333333",
            bg="white",
            anchor=tk.W,
        )
        name_label.pack(anchor=tk.W)

        desc_label = tk.Label(
            text_frame,
            text=tool["desc"],
            font=("Microsoft YaHei UI", 9),
            fg="#666666",
            bg="white",
            anchor=tk.W,
            justify=tk.LEFT,
        )
        desc_label.pack(anchor=tk.W)

        launch_btn = tk.Button(
            inner,
            text="启动",
            font=("Microsoft YaHei UI", 10),
            fg="white",
            bg=tool["color"],
            activebackground=tool["color"],
            activeforeground="white",
            relief=tk.FLAT,
            width=8,
            height=1,
            cursor="hand2",
            command=lambda t=tool: self._launch_tool(t),
        )
        launch_btn.pack(side=tk.RIGHT, padx=5)

        def on_enter(_event, c=card):
            c.configure(highlightbackground=tool["color"], highlightthickness=2)

        def on_leave(_event, c=card):
            c.configure(highlightbackground="#E0E0E0", highlightthickness=1)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for widget in [inner, icon_label, text_frame, name_label, desc_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def _launch_tool(self, tool: dict):
        script_path = self.script_dir / tool["script"]
        if not script_path.exists():
            messagebox.showerror("错误", f"找不到脚本文件:\n{script_path}")
            return

        try:
            args = [sys.executable, str(script_path)]
            if "args" in tool:
                args.extend(tool["args"])

            if sys.platform == "win32":
                subprocess.Popen(
                    args,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    cwd=str(self.script_dir),
                )
            else:
                subprocess.Popen(
                    args,
                    start_new_session=True,
                    cwd=str(self.script_dir),
                )
            self.iconify()
        except Exception as exc:
            messagebox.showerror("启动失败", f"无法启动工具:\n{exc}")

    def _show_help(self):
        help_text = """Writer Tool 工具箱说明

【创作工具】
- 资源管理器：管理项目资源、事件和 .writerproj 文件
- 助手配置编辑器：编辑浮动助手行为和 JSON 配置
- 事件分析工具：检查循环、死路径和缺失引用

【工程维护】
- 环境体检：检查 tkinter、核心依赖、关键入口文件
- 清理工作区：清掉 __pycache__、tmpclaude-*、dist、build
- 打包发布 ZIP：自动排除缓存与临时目录，输出干净压缩包

推荐顺序：
1. 覆盖升级包
2. 运行“环境体检”
3. 运行“清理工作区”
4. 正常启动主程序验证
5. 运行“打包发布 ZIP”生成对外包
"""
        dialog = tk.Toplevel(self)
        dialog.title("帮助")
        dialog.geometry("520x460")
        dialog.transient(self)

        text = tk.Text(
            dialog,
            wrap=tk.WORD,
            font=("Microsoft YaHei UI", 10),
            padx=15,
            pady=15,
        )
        text.pack(fill=tk.BOTH, expand=True)
        text.insert("1.0", help_text)
        text.configure(state=tk.DISABLED)

        ttk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=10)


def main():
    app = ToolsLauncher()
    app.mainloop()


if __name__ == "__main__":
    main()
