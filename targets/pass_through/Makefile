################################################################
#
# Makefile for pass_through P4 project
#
################################################################

export TARGET_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

include ../../init.mk

ifndef P4FACTORY
P4FACTORY := $(TARGET_ROOT)/../..
endif
MAKEFILES_DIR := ${P4FACTORY}/makefiles

# This target's P4 name
export P4_INPUT := p4src/pass_through.p4
export P4_NAME := pass_through

# Common defines targets for P4 programs
include ${MAKEFILES_DIR}/common.mk

# Put custom targets in pass_through-local.mk
-include pass_through-local.mk

all:bm

