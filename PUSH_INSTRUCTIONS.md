# 📤 Instructions pour Push sur GitHub

## Option A: GitHub CLI (Recommandé)

### 1. Installer GitHub CLI
```bash
# Télécharger et installer depuis:
# https://github.com/cli/cli/releases/latest
# Ou avec Homebrew (si installé):
brew install gh
```

### 2. Se connecter
```bash
gh auth login
# Choisir:
# - GitHub.com
# - HTTPS
# - Login with a web browser
```

### 3. Push
```bash
cd ~/Desktop/finary-icons-platform
git push -u origin main
```

---

## Option B: Personal Access Token

### 1. Créer un token
1. Va sur https://github.com/settings/tokens
2. Clique "Generate new token (classic)"
3. Nom: "finary-icons-platform"
4. Scopes: cocher **repo** (full control)
5. Clique "Generate token"
6. **COPIE LE TOKEN** (tu ne le reverras plus)

### 2. Push avec le token
```bash
cd ~/Desktop/finary-icons-platform
git push -u origin main

# Username: tahina-randria
# Password: [COLLE TON TOKEN ICI]
```

---

## Option C: SSH Key

### 1. Générer une clé SSH
```bash
ssh-keygen -t ed25519 -C "tahina@finary.com"
# Appuie sur Entrée 3 fois (pas de passphrase)
```

### 2. Copier la clé publique
```bash
cat ~/.ssh/id_ed25519.pub
# Copie tout le contenu
```

### 3. Ajouter sur GitHub
1. Va sur https://github.com/settings/keys
2. Clique "New SSH key"
3. Titre: "Mac Tahina"
4. Colle la clé
5. Clique "Add SSH key"

### 4. Changer le remote et push
```bash
cd ~/Desktop/finary-icons-platform
git remote set-url origin git@github.com:tahina-randria/finary-icons-platform.git
git push -u origin main
```

---

## ✅ Vérification

Une fois pushé, ouvre:
https://github.com/tahina-randria/finary-icons-platform

Tu devrais voir tous les fichiers ! 🎉
