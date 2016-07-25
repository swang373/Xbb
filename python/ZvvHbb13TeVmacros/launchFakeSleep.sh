cd ZvvHbb13TeVmacros && source launchFakeMET.csh && cd - && \
sleep 3h && \
source fakePrep.sh && \
sleep 1h && \
source fakeSys.sh && \
sleep 2h && \
source fakeFix.sh && \
sleep 2h && \
source fakePlot.sh \
>& logAll &


