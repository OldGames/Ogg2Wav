for /r %%I in (*.ogg) do (
	oggdec -b1 "%%I"
	del "%%I"
)
