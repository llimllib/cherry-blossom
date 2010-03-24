rsync -avuz -e ssh --safe-links \
--exclude ".git" --exclude "*.conf" --exclude ".*.swp" --exclude "static" \
. llimllib@billmill.org:~/cherry-blossom

#now copy the blog entries
rsync -avuz -e ssh --safe-links \
--exclude ".git" --exclude "*.conf" --exclude ".*.swp" \
~/code/personal_code/web/blog_entries llimllib@billmill.org:~/cherry-blossom

#and finally the static stuff
rsync -avuz -e ssh --safe-links \
--exclude ".git" \
ssh static/ llimllib@billmill.org:~/static
