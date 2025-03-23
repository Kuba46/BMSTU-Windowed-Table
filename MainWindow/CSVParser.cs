using System;
using System.Collections.Generic;
using System.IO;

public class CSVParser
{
    public List<List<string>> ParseCSV(string filePath)
    {
        var table = new List<List<string>>();

        try
        {
            using (var reader = new StreamReader(filePath))
            {
                string? line;
                while ((line = reader.ReadLine()) != null)
                {
                    var row = new List<string>();
                    var values = line.Split(',');
                    foreach (var value in values)
                    {
                        row.Add(value.Trim());
                    }
                    table.Add(row);
                }
            }
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Error reading CSV file: {ex.Message}");
        }

        return table;
    }
}