[bits 64]
[org 0x400880]

prologue:
	push rax
	push rdi
	push rsi
	push rdx
	push rcx
	push r8
	push r9

	xor eax, eax
	xor edi, edi
	xor esi, esi
	xor edx, edx
	xor ecx, ecx
	xor r8d, r8d

	mov edi, 0x400000
	mov esi, 0x1000
	mov dl, 7
	mov al, 0xa
	syscall

	mov edi, 0x600000
	mov esi, 0x1000
	mov dl, 3
	mov al, 0xa
	syscall

setup_registers:
	xor ecx, ecx
	push rcx
	push rcx

	mov edx, 0x2d2
	push rdx
	push 0x4004e0

	push rdx
	push 0x6004e0

	xor edx, edx
	mov dl, 0x68
	push rdx
	push 0x4007c0

	push rdx
	push 0x6007c0

	mov dl, 0xa0
	push rdx
	push 0x601020

outer: 
	pop rdi
	pop r8
	xor ecx, ecx
	test rdi, rdi
	je cleanup
load_ptr:
	lea rdx, [rdi + rcx]
	mov al, [rdx]
c1:
	cmp edx, 0x601000
	jb c2
	mov r9b, dl
	and dl, 0x3
	test dl, dl
	mov dl, r9b
	je decrypt
	jne jump
c2:
	test al, al
	je jump
decrypt:
	xor al, 0xa5
	mov [rdx], al
jump:
	inc rcx
	cmp rcx, r8
	jbe load_ptr
	jmp outer

cleanup:
	mov edi, 0x400000
	mov esi, 0x1000
	mov dl, 5
	mov al, 0xa
	syscall

	mov edi, 0x600000
	mov esi, 0x1000
	mov dl, 1
	mov al, 0xa
	syscall

	pop r9
	pop r8
	pop rcx
	pop rdx
	pop rsi
	pop rdi
	pop rax

	push 0x4004e0
	ret
