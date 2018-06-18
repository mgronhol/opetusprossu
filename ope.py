#!/usr/bin/python2

import Tkinter
from Tkinter import Tk, Frame, BOTH

import libope

PROCESSOR_SPEED_IN_HERTZ = 2.0

class App(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.parent.title("Opetusprossu")
		self.pack( fill = Tkinter.BOTH, expand = 1 )
		self.machine = libope.Machine()
		
		self.pc = 0
		self.prev_pc = 0
		
		self.running = False
		
		
		Tkinter.Label( self, text = "Memory" ).place( x = 10, y = 10 )
		
		self.mem_entries = []
		self.mem_intvars = []
		for i in range( libope.MEM_SIZE ):
			ivar = Tkinter.IntVar()
			Tkinter.Label( self, text = "%i" % i ).place( x = 10 + i*40, y = 30 )
			entry = Tkinter.Entry( self, textvariable = ivar, width = 4 )
			entry.place( x = 10 + i*40, y = 60 )
			self.mem_entries.append( entry )
			self.mem_intvars.append( ivar )
		
		
		Tkinter.Label( self, text = "Stack" ).place( x = 580, y = 100 )
		self.stack_entries = []
		self.stack_intvars = []
		
		for i in range( libope.STACK_SIZE ):
			ivar = Tkinter.IntVar()
			Tkinter.Label( self, text = "%i" %i ).place( x = 580, y = 500 - i*25 )
			entry = Tkinter.Entry( self, textvariable = ivar, width = 4 )
			entry.place( x = 610, y = 500 - i*25 )
			self.stack_entries.append( entry )
			self.stack_intvars.append( ivar )
		
		Tkinter.Label( self, text = "Program" ).place( x = 10, y = 100 )
		self.text = Tkinter.Text( self, width = 50, height = 20 )
		self.text.place( x = 10, y = 120 )
		
		Tkinter.Label( self, text = "Info" ).place( x = 10, y = 460 )
		self.info_var = Tkinter.StringVar()
		Tkinter.Entry( self, textvariable = self.info_var, width = 50 ).place( x = 70, y = 460 )
		
		Tkinter.Label( self, text = "Output" ).place( x = 10, y = 490 )
		self.output_var = Tkinter.StringVar()
		Tkinter.Entry( self, textvariable = self.output_var, width = 50 ).place( x = 70, y = 490 )
		
		Tkinter.Button( self, text = "Run", command = self.run_program ).place( x = 450, y = 450 )
		Tkinter.Button( self, text = "Step", command = self.step_program ).place( x = 450, y = 480 )
		Tkinter.Button( self, text = "Halt", command = self.halt_program ).place( x = 450, y = 510 )
		
		self.pc_var = Tkinter.IntVar()
		self.pc_var.set( 0 )
		Tkinter.Label( self, text = "Program counter" ).place( x = 450, y = 100 )
		Tkinter.Entry( self, textvariable = self.pc_var, width = 5 ).place( x = 480, y = 130)
		
		
		Tkinter.Label( self, text = "Registers").place( x = 450, y = 200 )
		self.reg_entries = []
		self.reg_intvars = []
		regs = sorted( self.machine.registers.keys() )
		for i in range( len( regs ) ):
			ivar = Tkinter.IntVar()
			Tkinter.Label( self, text = regs[i] ).place( x = 450, y = 225 + 25*i )
			entry = Tkinter.Entry( self, textvariable = ivar, width = 4 )
			entry.place( x = 480, y = 225 + 25*i )
			self.reg_entries.append( entry )
			self.reg_intvars.append( ivar )
	
	def update_memory( self ):
		for i in range( len( self.mem_intvars ) ):
			self.mem_intvars[i].set( self.machine.memory[i] )
	
	def update_stack( self ):
		for i in range( len( self.stack_intvars ) ):
			#self.mem_intvars[i].set( self.machine.memory[i] )
			if i < len( self.machine.stack ):
				self.stack_entries[i].config( state = Tkinter.NORMAL )
				self.stack_intvars[i].set( self.machine.stack[i] )
			else:
				self.stack_entries[i].config( state = "readonly" )
				self.stack_intvars[i].set( 0 )
				
	def update_registers( self ):
		regs = sorted( self.machine.registers.keys() )
		for i in range( len( regs ) ):
			self.reg_intvars[i].set( self.machine.registers[ regs[i] ] )
	
	def update_pc( self ):
		self.pc_var.set( self.pc )
		
	
	def execute_line( self ):
		txt = self.text.get(1.0, Tkinter.END)
		raw_lines = txt.splitlines()
		self.info_var.set( "" )
		
		lines = []
		self.actual_lines = {}
		n = 0
		for line in raw_lines:
			line = line.strip()
			if len( line ) > 0 and not line.startswith(";"):
				self.actual_lines[ len(lines) ] = n
				lines.append( line )
			n += 1
			
		if self.pc < len(lines ):
			
			self.text.tag_delete( "pc" )
			self.text.mark_unset( "matchStart" )
			self.text.mark_unset( "matchEnd" )
			
			
			start = self.text.index("%d.%d" % (self.actual_lines[self.pc] + 1, 0))
			end = self.text.index("%d.%s" % (self.actual_lines[self.pc] + 1, "end"))
			self.text.mark_set("matchStart", start)
			self.text.mark_set("matchEnd", end)
			
			self.text.tag_configure("pc", foreground="#ff0000" )
			self.text.tag_add("pc", "matchStart", "matchEnd")
			
			try:
				self.pc = self.machine.process( lines[self.pc], self.pc )
			except RuntimeError as re:
				self.info_var.set( re )
				self.running = False
		else:
			self.running = False
			self.info_var.set( "Done." )
			
		self.update_memory()
		self.update_stack()
		self.update_registers()
		self.update_pc()
		
		self.output_var.set( self.machine.output )
		
	def runner( self ):
		if self.running:
			self.execute_line()
			self.after( int(1000.0/PROCESSOR_SPEED_IN_HERTZ), self.runner )
	
	def run_program( self ):
		self.pc = 0
		self.machine = libope.Machine()
		self.update_memory()
		self.update_stack()
		self.update_registers()
		self.update_pc()
		self.output_var.set( self.machine.output )
		self.running = True
		self.runner()
		
	
	def step_program( self ):
		self.execute_line()
	
	def halt_program( self ):
		self.running = False
		self.pc = 0
		
		self.update_pc()
		
root = Tk()
app = App(root)
root.geometry("700x550+100+100")
root.mainloop()  


