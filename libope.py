#!/usr/bin/env python


OPCODES = [
'mov',
'load',
'store',
'push',
'pop',
'label',
'inc',
'dec',
'add',
'sub',
'mul',
'div',
'cmp',
'jmp',
'je',
'jne',
'jg',
'jl',
'out'
]


MEM_SIZE = 16
STACK_SIZE = 16

def check_params( op, parts, N ):
	if len(parts) != N:
		raise RuntimeError( "Invalid amount of operands for '%s' (got %i, expected %i)"% (op, len(parts), N) )

class Machine( object ):
	def __init__( self ):
		self.registers = {'r0':0, 'r1': 0, 'r2': 0}
		self.stack = []
		self.memory = [0]*MEM_SIZE
		self.compare = 0
		self.labels = {}
		self.output = ""
	
	def process( self, line, pos ):
		next_pos = pos + 1
		parts = line.strip().replace(",", " ").replace("\t", "").replace("  ", " ").replace( "  ", " " ).split()
		#print parts
		op = parts[0]
		params = parts[1:]
		if op not in OPCODES:
			raise RuntimeError("Invalid opcode '%s'" % op)
		
		if op == 'mov':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			if src in self.registers:
				self.registers[dst] = self.registers[src]
			else:
				try:
					value = int( src )
					self.registers[dst] = value
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'load':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			if src in self.registers:
				if self.registers[src] < 0 or self.registers[src] > MEM_SIZE:
					raise RuntimeError( "Invalid memory access @ %i" % self.registers[src] )
				
				self.registers[dst] = self.memory[ self.registers[src] ]
			else:
				try:
					value = int( src )
					if value < 0 or value > MEM_SIZE:
						raise RuntimeError( "Invalid memory access @ %i" % value )
					self.registers[dst] = self.memory[ value ]
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'store':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			
			if src not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % src )
			
			if dst in self.registers:
				if self.registers[dst] < 0 or self.registers[dst] > MEM_SIZE:
					raise RuntimeError( "Invalid memory access @ %i" % self.registers[dst] )
				else:
					self.memory[ self.registers[dst] ] = self.registers[ src ]
			else:
				try:
					value = int( dst )
					if value < 0 or value > MEM_SIZE:
						raise RuntimeError( "Invalid memory access @ %i" % value )
					self.memory[ value ] = self.registers[src]
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'push':
			check_params( op, params, 1 )
			src = params[0]
			if len( self.stack ) >= STACK_SIZE:
				raise RuntimeError( "Stack overflow" )
				
			if src in self.registers:
				self.stack.insert(0, self.registers[ src ] )
			else:
				try:
					value = int( src )
					self.stack.insert( 0, value )
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'pop':
			check_params( op, params, 1 )
			dst = params[0]
			if len( self.stack ) < 1:
				raise RuntimeError( "Stack underflow" )
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			
			self.registers[ dst ] = self.stack[0]
			self.stack = self.stack[1:]
			
		elif op == 'label':
			check_params( op, params, 1 )
			name = params[0]
			self.labels[ name ] = next_pos
		
		elif op == 'inc':
			check_params( op, params, 1 )
			dst = params[0]
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			self.registers[ dst ] += 1
		
		elif op == 'dec':
			check_params( op, params, 1 )
			dst = params[0]
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			self.registers[ dst ] -= 1
		
		elif op == 'add':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			
			if src in self.registers:
				self.registers[ dst ] += self.registers[ src ]
			else:
				try:
					value = int( src )
					self.registers[ dst ] += value
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'sub':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			
			if src in self.registers:
				self.registers[ dst ] -= self.registers[ src ]
			else:
				try:
					value = int( src )
					self.registers[ dst ] -= value
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'mul':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			
			if src in self.registers:
				self.registers[ dst ] *= self.registers[ src ]
			else:
				try:
					value = int( src )
					self.registers[ dst ] *= value
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
			
		elif op == 'div':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			
			if src in self.registers:
				self.registers[ dst ] /= self.registers[ src ]
			else:
				try:
					value = int( src )
					self.registers[ dst ] /= value
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
		
		elif op == 'cmp':
			check_params( op, params, 2 )
			dst = params[0]
			src = params[1]
			
			if dst not in self.registers:
				raise RuntimeError( "Invalid operand '%s'" % dst )
			
			if src in self.registers:
				if self.registers[dst] == self.registers[src]:
					self.compare = 1
				elif self.registers[dst] > self.registers[src]:
					self.compare = 2
				elif self.registers[dst] < self.registers[src]:
					self.compare = 3
				else:
					self.compare = 0
			else:
				try:
					value = int( src )
					if self.registers[dst] == value:
						self.compare = 1
					elif self.registers[dst] > value:
						self.compare = 2
					elif self.registers[dst] < value:
						self.compare = 3
					else:
						self.compare = 0
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % src )
			
		elif op == 'jmp':
			check_params( op, params, 1 )
			dst = params[0]
			
			if dst not in self.labels:
				raise RuntimeError( "Invalid label '%s'" % dst )
			else:
				next_pos = self.labels[ dst ]
		
		elif op == 'je':
			check_params( op, params, 1 )
			dst = params[0]

			if dst not in self.labels:
				raise RuntimeError( "Invalid label '%s'" % dst )
			else:
				if self.compare == 1:
					next_pos = self.labels[ dst ]

		elif op == 'jne':
			check_params( op, params, 1 )
			dst = params[0]

			if dst not in self.labels:
				raise RuntimeError( "Invalid label '%s'" % dst )
			else:
				if self.compare != 1:
					next_pos = self.labels[ dst ]
		
		elif op == 'jg':
			check_params( op, params, 1 )
			dst = params[0]

			if dst not in self.labels:
				raise RuntimeError( "Invalid label '%s'" % dst )
			else:
				if self.compare == 2:
					next_pos = self.labels[ dst ]

		elif op == 'jl':
			check_params( op, params, 1 )
			dst = params[0]

			if dst not in self.labels:
				raise RuntimeError( "Invalid label '%s'" % dst )
			else:
				if self.compare == 3:
					next_pos = self.labels[ dst ]
		
		elif op == 'out':
			check_params( op, params, 1 )
			dst = params[0]
			
			if dst in self.registers:
				self.output += chr( self.registers[dst] )
			else:
				try:
					value = int( dst )
					self.output += chr( value )
				except ValueError:
					raise RuntimeError( "Invalid operand '%s'" % dst )
		
		return next_pos



