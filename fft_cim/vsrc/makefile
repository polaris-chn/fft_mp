.PHONY: sim, verdi, clean

PROJECT = test

VCS = 	vcs \
		-full64 \
		-R \
		-timescale=1ns/1ns \
		-debug_all \
		-fsdb \
		+define+FSDB \
		+v2k \
		-sverilog \
		-LDFLAGS -Wl,--no-as-needed \

VERDI =	verdi \
		-sv \
		-nologo \
		-play setting.tcl \
		-ssf ${PROJECT}.fsdb \


sim:
		make clean
		${VCS} -f ${PROJECT}.f

verdi:
		${VERDI} -f ${PROJECT}.f &

clean:
		rm -rf ./csrc ./DVEfiles *.daidir *.log simv* *.key *.vpd \
				verdi* novas* *.fsdb
