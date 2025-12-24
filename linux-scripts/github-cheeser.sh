#!/bin/bash
MAX_COMMITS_PER_DAY=5
FROM_DAYS_AGO=177
TO_DAYS_AGO=84

for day_ago in $(seq $TO_DAYS_AGO $FROM_DAYS_AGO);
do
	past_day_date=$(date --date="$day_ago days ago" +%u)
	if [ $past_day_date -gt 5 ]; then
		echo "Skipping weekend day $past_day_date"
		continue
	fi
	commits_per_day=$(((RANDOM%MAX_COMMITS_PER_DAY)+1))

	printf "\nCreating $commits_per_day commits for $day_ago days ago"
	for commit in $(seq 1 $commits_per_day);
	do
		git commit --allow-empty --date "$day_ago day ago" -m "Cheesed on $(date +%Y-%m-%d-%H:%M:%S)"
	done
done
