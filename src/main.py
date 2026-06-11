if __name__ == "__main__":
    while True:
    if not threading_service.is_full():
        command = await crud.poll_pending()
        if command:
            threading_service.run(cmd_handler.execute, command)
    await asyncio.sleep(0.1)  # evita busy-loop