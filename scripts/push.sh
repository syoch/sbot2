#!/bin/sh

git push
git -C libs/eval push origin HEAD:main
git -C libs/expr_conv push origin HEAD:main