<div align="center">
  <img src="./assets/5142438-cute-baby-tigre-vettoriale.jpg" width=400 style="border-radius: 50%; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"/>
  <h1 style="font-size: 4em; color: #ff6f00; text-shadow: 2px 2px 4px #000000;">🐯tigr81</h1>
  <p style="font-size: 1.5em; color: #4a4a4a;">A Project Scaffolder for HUMANS. My name is tigr81 that can be read as "tigr-ottone" more user-friendly for Italian developers.</p>
</div>

## 🚀 What is tigr81?

Tigr81 is a powerful and user-friendly project scaffolder that empowers you to kickstart your projects with just a single command. Designed with simplicity and ease of use in mind, tigr81 is the perfect companion for developers looking to streamline their project setup process. Currently, tigr81 supports three types of projects:

- 🌐 fastapi
- 📦 poetry_pkg
- ⚛️ prime-react
- 🔜 more is coming soon!

## 📥 How to install tigr81?

Installing tigr81 is a breeze! Simply use pip, the Python package installer, and run the following command:

```bash
pip install tigr81
```

And voila! You're ready to embark on your project scaffolding journey with tigr81.

## 🤔 How to use tigr81?

To discover the full potential of tigr81 and learn how to harness its capabilities, simply run the following command:

```bash
tigr81 --help
```

This command will provide you with a comprehensive guide on how to utilize tigr81 effectively.

## 🌟 How to create a new project?

Creating a new project with tigr81 is as easy as 1, 2, 3! Just run the following command:

```bash
tigr81 scaffold <project_type>
```

Replace `<project_type>` with the desired project type from the available options (fastapi, poetry_pkg, prime-react).

For example, to create a new FastAPI project, simply execute:

```bash
tigr81 scaffold fastapi
```

Follow the interactive prompts, and tigr81 will guide you through the process of setting up your project effortlessly.

---

<div align="center">
  <p style="font-size: 1.2em; color: #4a4a4a;">Start your projects with ease using tigr81 - the project scaffolder that roars with simplicity and power! 🐯💪</p>
</div>

## 🚀 How to Deploy a New Version of tigr81?

Deploying a new version of tigr81 is streamlined through a structured workflow to ensure stability and ease of deployment. Follow these steps:

1. **Open a Feature Branch**: Begin by creating a new branch from `main` for your new feature or fix:

   ```bash
   git checkout -b feat/<your-feature-name>
   ```

2. Implement Your Changes: Add, commit, and push your changes to your feature branch.
3. Create a Pull Request (PR) to `main`:
   - Open a PR targeting the `main` branch.
   - Include relevant information in the PR description to help reviewers understand your changes.
4. Run the CI/CD Workflow Manually: Once your PR is merged into `main`, manually trigger the CI/CD workflow to deploy the new version.
5. Monitor the Deployment: After initiating the workflow, monitor its progress to ensure successful deployment.
