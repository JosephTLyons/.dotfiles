excluded_items=(
    ".DS_Store"
    ".git"
    ".gitignore"
)

for file in .??*; do
    for excluded_item in ${excluded_items[@]}; do
        should_skip=false

        if [ $file == $excluded_item ]; then
            should_skip=true
            break
        fi
    done

    if [ "$should_skip" = false ]; then
        ln -s "${HOME}/.dotfiles/${file}" "${HOME}/${file}";
    fi
done

ln -s "${HOME}/.dotfiles/.zprofile" "${HOME}/.profile"
