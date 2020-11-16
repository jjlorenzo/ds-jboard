#!/usr/bin/env crun

require "colorize"
require "option_parser"

Colorize.on_tty_only!

ParentIO = Process::Redirect::Inherit

ServicesBck = [
  {"bck-conn", "db-8200", "poetry install", "poetry run jboard create-tables"   },
  {"bck-djrf", "db-8300", "poetry install", "poetry run django-admin.py migrate"},
] of Tuple(String, String, String, String)

ServicesFrn = [
  {"frn-vaui", "yarn install", "yarn build"},
] of Tuple(String, String, String)

struct SettingsStruct
  property depsinstall = true
  property development = true
  property dockerbuild = true
  property initdtabase = true
end

Settings = SettingsStruct.new

OptionParser.parse ARGV.clone do |parser|
  parser.banner = "usage: reset-stack"
  parser.on "--no-depsinstall", "!" { Settings.depsinstall = false }
  parser.on "--no-development", "!" { Settings.development = false }
  parser.on "--no-dockerbuild", "!" { Settings.dockerbuild = false }
  parser.on "--no-initdtabase", "!" { Settings.initdtabase = false }
  parser.on "-h", "?" do
    STDOUT.puts parser
    exit 0
  end
  parser.invalid_option do |flag|
    STDERR.puts "[?] Ignoring unknown flag #{flag.colorize(:white)}".colorize(:red)
  end
end

begin
  prun docker "build --tag=dstreet/jboard ." if Settings.dockerbuild
  if Settings.initdtabase
    prun compose "down --remove-orphans --volumes"
  else
    prun compose "down --remove-orphans"
  end
  ServicesBck.each do |name, dbname, install_cmd, migrate_cmd|
    prun compose_run "#{name} #{install_cmd}"
  end if Settings.depsinstall
  ServicesFrn.each do |name, install_cmd, build_cmd|
    prun compose_run "#{name} #{install_cmd}"
    prun compose_run "#{name} #{build_cmd}"
  end if Settings.depsinstall
  begin
    proc = pnew compose_run "--name=postgres --service-ports postgres postgres-server.crun --log-connections"
    begin
      sleep 8
      until (prun compose "run --rm postgres pg_isready -hpostgres -Upostgres").success?
        sleep 1
      end
      ServicesBck.each do |name, dbname, install_cmd, migrate_cmd|
        prun compose "run --rm --no-deps #{name} dropdb -hpostgres -Upostgres --if-exists #{dbname}"
        prun compose "run --rm --no-deps #{name} createdb -hpostgres -Upostgres --template=template0 #{dbname}"
        prun compose "run --rm --no-deps #{name} #{migrate_cmd}"
        prun compose "run --rm --no-deps #{name} psql -hpostgres -Upostgres -d#{dbname} -c\\dt"
      end
    ensure
      sleep 4
      proc.terminate
      proc.wait
    end
  end if Settings.initdtabase
  pexe compose "up --no-deps postgres #{(ServicesBck + ServicesFrn).map{ |e| e[0] }.join(" ")}".strip
rescue
  prun compose "down --volumes --remove-orphans"
end

def compose(args : String? = nil)
  cmd = [] of String
  cmd << "docker-compose"
  cmd << "--file=docker-compose.yml" unless Settings.development
  cmd += args.split " " if args
  cmd
end

def compose_run(args : String)
  cmd = compose
  cmd << "run"
  cmd << "--rm"
  cmd << "--no-deps"
  cmd += args.split " "
end

def docker(args : String)
  cmd = [] of String
  cmd << "docker"
  cmd += args.split " "
end

def pexe(cmd : Array(String))
  puts "\n[+] #{cmd}\n\r".colorize(:green)
  Process.exec command: cmd[0], args: cmd[1..-1], input: ParentIO, output: ParentIO, error: ParentIO
end

def pnew(cmd : Array(String))
  puts "\n[+] #{cmd}\n\r".colorize(:yellow)
  Process.new command: cmd[0], args: cmd[1..-1], input: ParentIO, output: ParentIO, error: ParentIO
end

def prun(cmd : Array(String))
  puts "\n[+] #{cmd}\n\r".colorize(:white)
  Process.run command: cmd[0], args: cmd[1..-1], input: ParentIO, output: ParentIO, error: ParentIO
  raise Exception.new "Exiting with failure status due to previous errors." unless $?.success?
  $?
end
