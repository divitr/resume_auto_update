#!/bin/bash

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"
TEX_FILES=()

git pull origin main >/dev/null 2>&1

proccess_dir() {
	local dir="$1"
	for item in "$dir"/*; do
		if [ -d "$item" ]; then
			proccess_dir "$item"
		elif [ -f "$item" ]; then
			if [[ "$item" == *.tex ]]; then
                		TEX_FILES+=("$item")
            		fi
		fi
	done
}

proccess_dir "$DIR"

push_to_git() {
	cd "$DIR"
	git add .
	commit_msg="auto_update on $(date +'%Y-%m-%d %H:%M:%S')"
	git commit -m "$commit_msg" >/dev/null 2>&1
	git push origin main >/dev/null 2>&1
}

recompile_resumes() {
    for file in "${TEX_FILES[@]}"; do
    	if [[ "$file" == *Divit_Rawal.tex ]]; then
			dir_path=$(dirname "$file")
			cd "$dir_path"
			pdflatex Divit_Rawal.tex >/dev/null 2>&1
			cd ..
		fi
    done
	push_to_git
}

check_recompile() {
    	local threshold="$1"
    	local current_time=$(date +%s)

    	for item in "${TEX_FILES[@]}"; do
        	local mod_time=$(date -r "$item" +%s)
        	if [ "$((current_time - mod_time))" -lt "$threshold" ]; then
            		recompile_resumes
            		break
        	fi
    	done
}

threshold_time=6

check_recompile "$threshold_time"

git pull origin main > /dev/null 2>&1
