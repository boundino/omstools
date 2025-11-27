CXX = g++
# CXXFLAGS += -O2 -Wall -Werror -Wextra
ROOTFLAGS := `root-config --cflags --libs` -lEG -I$(HOME) -std=c++20 -w

BUILDDIR = ./build

SRCS  = $(wildcard *.cc)
EXES  = $(patsubst %.cc,%,$(SRCS))
DEPS  = $(patsubst %.cc,$(BUILDDIR)/%.d,$(SRCS))

.PHONY: all clean

all: $(EXES)

%: %.cc
	@mkdir -p $(BUILDDIR)/$(@D)
	$(CXX) $(ROOTFLAGS) $(CXXFLAGS) -MMD -MF $(BUILDDIR)/$(@D)/$(*F).d $< -o $@

clean:
	@$(RM) $(EXES) $(DEPS)
	@rm -rf $(BUILDDIR)/*

-include $(DEPS)
