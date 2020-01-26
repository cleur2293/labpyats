" enable syntax highlighting
syntax enable
" "
" " " show line numbers
set number
" "
" " " set tabs to have 4 spaces
set ts=4
" "
" " " indent when moving to the next line while writing code
set autoindent
" "
" " " expand tabs into spaces
set expandtab
" "
" " " when using the >> or << commands, shift lines by 4 spaces
set shiftwidth=4
" "
" " " show a visual line under the cursor's current line
set cursorline
" "
" " " show the matching part of the pair for [] {} and ()
set showmatch
" "
" " " enable all Python syntax highlighting features
let g:python3_host_prog='/home/cisco/pyats/bin/python3'
let python_highlight_all = 1

let g:deoplete#sources#jedi#show_docstring = 1

call plug#begin()
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
Plug 'SkyLeach/pudb.vim'
Plug 'w0rp/ale' " using flake8
Plug 'zchee/deoplete-jedi' " autocompletion source
call plug#end()

nnoremap <silent> <unique> <leader>d :PUDBLaunchDebuggerTab<CR><CR>
nnoremap <silent> <leader>b :PUDBToggleBreakPoint<CR>
nnoremap <silent> <leader>c :PUDBClearAllBreakpoints<CR>

