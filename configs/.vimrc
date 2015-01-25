set nocompatible
set number
set autoindent
set expandtab
set shiftwidth=4
set softtabstop=4
set whichwrap+=h,l,<,>,[,]
syntax enable
set backspace=indent,eol,start
set hlsearch
autocmd InsertEnter * set number
autocmd InsertEnter * colorscheme molokai
autocmd InsertEnter * set background=dark
set timeoutlen=0
set ruler
set t_Co=256
colorscheme molokai
set background=dark
"let g:molokai_original=1

" enable filetype detection
filetype on
filetype plugin on
filetype indent on " file type based indentation

" setup makefile
autocmd Filetype make set noexpandtab shiftwidth=8 softtabstop=0

" for C-like programming where comments have explicit end
" characters, if starting a new line in the middle of a comment
" automatically insert comment leader characters
autocmd Filetype c,cpp,java set formatoptions+=ro
autocmd Filetype c, set omnifunc=ccomplete#Complete
