# Poyo - CLI Command Alias Manager

Poyo is a simple command alias manager for the terminal. It allows you to store frequently used commands under short aliases, making your workflow more efficient.

## 🚀 Features
- **Save** long commands as short aliases
- **Run** saved aliases instantly
- **List** all stored aliasess
- **Update** existing aliases
- **Delete** aliases when no longer needed
s
## 📦 Installation
### 1. Clone the repository
```sh
git clone https://github.com/jamisonleah/poyo.git
cd poyo
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```

### 3. Make it executable
```sh
chmod +x poyo.py
mv poyo.py ~/.local/bin/poyo
```
Ensure `~/.local/bin` is in your `PATH`:
```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc  # or `source ~/.zshrc` for zsh users
```

## 🛠 Usage

### Add a new alias
```sh
poyo add <key> "<command>"
```
Example:
```sh
poyo add ll "ls -lah"
```

### Run an alias
```sh
poyo run <key>
```
Example:
```sh
poyo run ll
```
(Executes `ls -lah`)

### List all aliases
```sh
poyo list
```

### Update an alias
```sh
poyo update <key> "<new_command>"
```
Example:
```sh
poyo update ll "ls -l"
```

### Delete an alias
```sh
poyo delete <key>
```
Example:
```sh
poyo delete ll
```

## 📌 Phase 2 Enhancements
Here are some planned improvements for Poyo:
- **Import/export functionality**: Easily back up and restore aliases.
- **Autocomplete support**: Enable tab completion for saved aliases.


## 📜 License
Poyo is open-source and available under the MIT License.

## 📝 Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## 💬 Support
If you run into any issues, open an issue in the GitHub repository or reach out on the discussion forum.

