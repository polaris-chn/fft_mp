.PHONY: sim, verdi, clean

PROJECT = fft_multipoint

VCS	= 	vcs \
		-full64 \
		-R \
		-timescale=1ns/1ns \
		-debug_all \
		-fsdb \
		+define+FSDB \
		+v2k \
		-sverilog \


VERDI =	verdi \
		-sv \
		-nologo \
		-play setting.tcl \
		-ssf ${PROJECT}.fsdb \


sim:
		# make clean
		${VCS} -f ${PROJECT}.f

verdi:
		${VERDI} -f ${PROJECT}.f &


clean:
		rm -rf ./csrc ./DEVfiles *.daidir *.log simv* *.key *.vpd \
				verdi* novas* *.fsdb *.swp
