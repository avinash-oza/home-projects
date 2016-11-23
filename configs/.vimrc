"
" dotvim : https://github.com/dotphiles/dotvim
"
" Setup vim and load required plugins before dotvim
"
" Authors:
"   Ben O'Hara <bohara@gmail.com>
"

" Call dotvim
source ~/.vim/dotvim.vim

if has("user_commands")
  set nocompatible
  filetype off
  set rtp+=~/.vim/bundle/vundle/
  call vundle#rc()
  "let g:vundles=['general', 'git', 'hg', 'programming', 'completion', 'ruby', 'python', 'misc']
  let g:vundles=['general', 'python', 'programming', 'git']
  "let g:neocomplcache_enable_at_startup = 1
  " Load 'vundles'
  source ~/.vim/vundles.vim
  " Add extra bundles here...
  " Bundle 'reponame'
  Bundle 'airblade/vim-gitgutter'
  Bundle 'spf13/vim-markdown'
  Bundle 'powerline/powerline'
  Bundle 'vim-airline/vim-airline-themes'
endif

" Override colorscheme from base16
let g:dotvim_colorscheme = 'base16-default'

" Customize to your needs...

