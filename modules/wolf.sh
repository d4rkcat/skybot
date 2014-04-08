#!/bin/bash
API_KEY=64Y5LQ-V89Y2JWTG4
q=$(echo ${*} | sed 's/+/%2B/g' | tr '\ ' '\+')
result=$(curl -s "http://api.wolframalpha.com/v2/query?input=${q}&appid=${API_KEY}&format=plaintext")
result=`echo "${result}" \
	| tr '\n' '\t' \
	| sed -e 's/<plaintext>/\'$'\n<plaintext>/g' \
	| grep -oE "<plaintext>.*</plaintext>|<pod title=.[^\']*" \
	| sed -e 's!<plaintext>!!g; \
		s!</plaintext>!!g; \
		s!<pod title=.!!g; \
		s!<pod title=.!!g; \
		s!\&amp;!\&!g; \
		s!\&lt;!<!g; \
		s!\&gt;!>!g; \
		s!\&quot;!"!g' \
		-e "s/\&apos;/'/g" \
	| tr '\t' '\n' \
	| sed  '/^$/d; \
		s/\ \ */\ /g; \
		s/\\\:/\\\u/g'`
echo -e "${result}" > /tmp/wolf
