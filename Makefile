#!/bin/bash
BASE:=$(PWD)

all: test

test:
	cd $(BASE)/chat-paper && make test
	cd $(BASE)/chat-reviewer && make test

install:
	conda env create -f $(BASE)/environment.yml -y

clean:
	rm -rf $(BASE)/__pycache__
	cd $(BASE)/chat-paper && make clean
	cd $(BASE)/chat-reviewer && make clean

