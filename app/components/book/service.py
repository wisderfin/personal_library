import aiofiles


async def save_md_to_src(file, name):
    async with aiofiles.open(f'src/book/{name}.md', 'w+') as md:
        await md.write(file)