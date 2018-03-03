import re, sys

def main(infile, outfile):
    input = open(infile, "r")
    out = open(outfile,"w")
    for line in input:
        process = False
        for item in ('BEGIN TRANSACTION','COMMIT',
                 'sqlite_sequence','DROP INDEX', 'PRAGMA'):
            if item in line: break
        else: process = True

        if not process:
            continue

        line = line.replace('"','`')

        if 'CREATE TABLE' in line:
            m = re.search('CREATE TABLE `([a-z_]*)`(.*)', line)
            if m:
                name, sub = m.groups()
                line = '''DROP TABLE IF EXISTS %(name)s;\nCREATE TABLE IF NOT EXISTS %(name)s%(sub)s\n'''
                #line = "DROP TABLE IF EXISTS"
                line = line % dict(name=name, sub=sub)
            else:
                print("Something is very wrong, look at this line {}".format(line))
                sys.exit(1)

            line_split = line.split(',')
            newline = ''
            foreignkeys = ''
            fk_flag = False

            for item in line_split:
                if 'REFERENCES' in item:
                    fk_flag = True
                    match = re.match(r'(.*)(\`.*\`) (.*) (.*REFERENCES) (\`.*\`) \((\`.*\`)\)(.*)', item, flags=0)
                    
                    if match:
                        newline = newline + match.group(2) + ' ' + match.group(3) + ','
                        newline = newline + "FOREIGN KEY(" + match.group(2) + ") REFERENCES " + match.group(5) + " (" + match.group(6) + "),"
                    else:
                        print("Something is very wrong, look at this item {}".format(item))
                        sys.exit(1)
                else:
                    fk_flag = False
                    newline = newline + item +','
            if fk_flag:
                #newline = newline + foreignkeys
                line = newline[:-1] + ');\n'
            else:
                line = newline[:-1]

        if 'CREATE INDEX' in line or 'CREATE UNIQUE INDEX' in line:
            line = line.replace('IF NOT EXISTS', '')

        line = line.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
        out.write(line)
    out.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid Arguments")
    main(sys.argv[1], sys.argv[2])
