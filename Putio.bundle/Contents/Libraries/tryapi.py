import putio2
client = putio2.Client('8dd3c2049ab911e194c308002708c8ea')

# files = client.File.list(parent_id=23)
# print files

# files = client.File.list(parent_id=0)
# print files

f = client.File.GET(id=19)
print f.stream_url
