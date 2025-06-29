# XsView - 一个疾速的、美观的Vue前端面板框架

## 简介

XsView 是SiiWay团队的一个基于 Vue 3、Vite 和 Naive UI 构建的轻量级前端面板框架。它从Xscore中精简而来，移除了所有与具体业务逻辑相关的组件和代码，仅保留了核心的UI框架、路由管理、状态管理以及基础的系统设置和关于页面。这使得 XsView 成为一个理想的起点，可用于快速搭建各类管理后台、数据展示面板或个人项目。

## 特性

*   **“新新”向荣**: 采用最新、最快的前端技术栈，提供卓越的开发体验和构建性能。
*   **Naive UI**: 基于 Vue 3 的一套完整、可定制的UI组件库，提供美观且高性能的界面元素。
*   **精简核心**: 保留了基础的框架结构，极度方便二次开发。
*   **响应式布局**: 适配不同屏幕尺寸，提供良好的用户体验。
*   **高度客制化**: 内置暗黑模式切换功能，颜色主题切换功能，即将引入液态玻璃样式。
*   **大道至简**: 我团队大部分应用均考虑了文件体积，因为我们所使用的CDN完全不能满足一个中小型网站的速度要求，所以，我们尽最大可能减小了代码量，如你所见，整个布局不到10kb，子组件路由不超过5kb，当你体验tree-shaking的时候，好好感谢我们吧。(实测Xscore(本项目原型)打包总大小878kb)

## 项目结构

```
.github/
public/
├── fonts/ # 字体文件(随你删)
├── vite.svg # 网站图标
src/
├── assets/ # 静态资源
├── components/ # 核心UI组件 (Home, Settings, About, BackToTop, SkeletonScreen, ThemeSettings)
├── layouts/ # 布局组件 (Header, ResponsiveMenu, Sidebar)
├── router/ # 路由配置
├── stores/ # Pinia状态管理模块(可更换)
├── utils/ # 工具函数
├── App.vue # 主应用组件
├── main.ts # 应用入口文件
├── vite-env.d.ts # Vite环境变量声明
package.json # 项目依赖和脚本配置
index.html # HTML入口文件
vite.config.ts # Vite配置
README.md # 本文件
```

## 安装与运行

1.  **克隆仓库**

    ```bash
    git clone https://github.com/siiway/XsView
    cd xsview
    ```

2.  **安装依赖**

    ```bash
    npm install
    # 或者使用 yarn
    # yarn install
    # 或者使用 pnpm
    # pnpm install
    *在组件库有更新而本框架没有守时更新的情况下请加--legacy-peer-deps以安装依赖
    ```

3.  **运行开发服务器**

    ```bash
    npm run dev
    ```

    项目将在本地 `http://localhost:3003` 启动。(可自行修改运行端口)

4.  **构建生产版本**

    ```bash
    npm run build
    ```
    构建后的文件将输出到 `dist` 目录。

## 如何扩展

XsView 的设计理念是提供一个干净的起点。你可以根据自己的需求进行以下扩展：

*   **添加新页面**: 在 `src/components` 目录下创建新的 Vue 组件，并在 `src/router/index.ts` 中添加对应的路由配置。
*   **集成API**: 使用 `axios` 或其他HTTP客户端库与后端API进行交互。
*   **自定义UI**: 根据 Naive UI 的文档，定制主题、组件样式或添加更多组件。
*   **状态管理**: 在 `src/stores` 中创建新的 Pinia 模块来管理应用状态。

## 许可证

本项目在众多项目的启发下构成，具体的开源协议请等待后期提出。

## 贡献

欢迎任何形式的贡献！如果你有任何建议、bug报告或功能请求，请通过 GitHub Issues 提交。

