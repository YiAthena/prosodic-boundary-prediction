#include "netcdf.h"
#include <iostream>
#include <stdexcept>
#include <stdlib.h>
#include <vector>
#include <string.h>
#include <fstream>
#include <sstream>

using namespace std;

int readNcDimension(int ncid, const char *dimName)
{
	int ret;
	int dimid;
	size_t x;

	if ((ret = nc_inq_dimid(ncid, dimName, &dimid)) || (ret = nc_inq_dimlen(ncid, dimid, &x)))
		throw std::runtime_error(std::string("Cannot get dimension '") + dimName + "': " + nc_strerror(ret));

	return (int)x;
}

void readnc(char *filename)
{
	int ncid;
	int ret;
	ret = nc_open(filename, NC_WRITE, &ncid);

	int numSeqs = readNcDimension(ncid, "numSeqs");
	cout << "numSeqs:" << numSeqs << endl;

	int numTimesteps = readNcDimension(ncid, "numTimesteps");
	cout << "numTimesteps:" << numTimesteps << endl;

	int inputPattSize = readNcDimension(ncid, "inputPattSize");
	cout << "inputPattSize:" << inputPattSize << endl;

	int numLabels = readNcDimension(ncid, "numLabels");
	cout << "numLabels:" << numLabels << endl;

	int maxLabelLength = readNcDimension(ncid, "maxLabelLength");
	cout << "maxLabelLength:" << maxLabelLength << endl;

	int maxTargStringLength = readNcDimension(ncid, "maxTargStringLength");
	cout << "maxTargStringLength:" << maxTargStringLength << endl;

	int maxSeqTagLength = readNcDimension(ncid, "maxSeqTagLength");
	cout << "maxSeqTagLength:" << maxSeqTagLength << endl;

}

void Usage_prosody(char *exe)
{
	cerr << "Usage: " << exe << ": inputfile targetfile frame ncfile" << endl;
}

// 将string按照delimiter分开
void split(string str, const char* delimiter, vector<string>& tokens)
{
	tokens.clear();
	char *p;
	char *buf = const_cast<char*>(str.c_str());
	p = strtok(buf, delimiter);
	while (p != NULL)
	{
		tokens.push_back(p);
		p = strtok(NULL, delimiter);
	}
}

int getPattSize(char * filename)
{
	ifstream file(filename);
	string buf;
	getline(file, buf);
	vector<string> Patt;
	split(buf, " ", Patt);
	return Patt.size();
}

int writenc_prosody(int argc, char *argv[])
{
	Usage_prosody(argv[0]);

	char * inputfile = argv[1];
	char * targetfile = argv[2];
	char * frame = argv[3];
	char * ncfile = argv[4];

	//dimensions
	int numSeqs = 0; // number of sequences
	int numTimesteps = 0; // number of time stpes
	int inputPattSize = 0; // input pattern size
	int numLabels = 0; // number of labels
	int maxLabelLength = 0; // max label length

	//add 2015/11/2
	int maxSeqTagLength = 0; //max sequence tag length


	//variables
//	vector<string> labels; //(numLabels, maxLabelLength) let's keep multi-task classification in mind ...
	vector<int> seqLengths; //(numSeqs)
	vector<int> targetClasses; //(numTimesteps)
	//vector<vector<double> > inputs; //(numTimesteps, inputPattSize)
	
	// add 2015/11/2
	unsigned int seqTags = 10000;

	// read frame
	ifstream fframe(frame);
	string buf;
	while (!fframe.eof())
	{
		getline(fframe, buf);
		if (buf.length() == 0)
		{
			continue;
		}
		int n = atoi(buf.c_str());
		numSeqs++;
		numTimesteps += n;
		seqLengths.push_back(n);
	}

	// convert seq len vector to C array
	int* seqLenArr = new int[numSeqs];
	for (int i = 0; i < numSeqs; i++)
	{
		seqLenArr[i] = seqLengths[i];
	}

	// input output size
	inputPattSize = getPattSize(inputfile);
	numLabels = getPattSize(targetfile);

	//maxLabelLength
	maxLabelLength = 1;

	//add 2015/11/2
	maxSeqTagLength = 5;

	// nc head
	int ret;
	int ncid;
	if ((ret = nc_create(ncfile, NC_NETCDF4, &ncid)) != NC_NOERR)
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}

	// dimensions
	// numSeqs
	int nseq_dimid;
	if ((ret = nc_def_dim(ncid, "numSeqs", numSeqs, &nseq_dimid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// numTimesteps
	int nt_dimid;
	if ((ret = nc_def_dim(ncid, "numTimesteps", numTimesteps, &nt_dimid)) != NC_NOERR)
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	//inputPattSize
	int input_size_dimid;
	if ((ret = nc_def_dim(ncid, "inputPattSize", inputPattSize, &input_size_dimid)) != NC_NOERR)
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// numLabels
	int num_labels_dimid;
	if ((ret = nc_def_dim(ncid, "numLabels", numLabels, &num_labels_dimid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// add 2015/11/2
	// maxSeqTagLength
	int mstl_dimid;
	if ((ret = nc_def_dim(ncid,"maxSeqTagLength",maxSeqTagLength, &mstl_dimid)) != NC_NOERR)
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}

	//variables
	// seqLengths
	int seqLengths_dimids[] = { nseq_dimid };
	int seqLengths_varid;
	if ((ret = nc_def_var(ncid, "seqLengths", NC_INT, 1, seqLengths_dimids, &seqLengths_varid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// targetClasses
	int labels_varid;
	int labels_dimids[] = { nt_dimid };
	if ((ret = nc_def_var(ncid, "targetClasses", NC_INT, 1, labels_dimids, &labels_varid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// inputs
	int input_dimids[] = { nt_dimid, input_size_dimid };
	int inputs_varid;
	if ((ret = nc_def_var(ncid, "inputs", NC_FLOAT, 2, input_dimids, &inputs_varid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// add 2015/11/2
	// seqTags
	int seqTags_dimids[] = { nseq_dimid, mstl_dimid };
	int seqTags_varid;
	if ((ret = nc_def_var(ncid, "seqTags", NC_CHAR, 2, seqTags_dimids, &seqTags_varid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}


	// exit definition mode to write variable contents.
	if ((ret = nc_enddef(ncid)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}

	// write nc file
	// add 2015/11/2
	for (int s = 0; s < numSeqs; ++s) 
	{
		stringstream stream;
		stream << seqTags;
		string ss = stream.str();
		size_t start[] = { s, 0 };
		size_t count[] = { 1, ss.size() };
		if ((ret = nc_put_vara_text(ncid, seqTags_varid, start, count, ss.c_str())) != NC_NOERR) 
		{
			cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
			return ret;
		}
	}
	// seqLengths
	if ((ret = nc_put_var_int(ncid, seqLengths_varid, seqLenArr)) != NC_NOERR) 
	{
		cerr << "Could not create NC file: " << nc_strerror(ret) << endl;
		return ret;
	}
	// inputs, targetPatterns
	ifstream input(inputfile);
	ifstream target(targetfile);
	size_t t = 0;
	char * tmp = new char[1];
	for (int s = 0; s < numSeqs; s++)
	{
		if (s > 0 && s % 100 == 0)
		{
			cout << s << endl;
		}
		
		// define input buf
		float * input_buf = new float[inputPattSize * seqLengths[s]];
		// read input buf
		for (size_t i = 0; i < inputPattSize * seqLengths[s]; i++)
		{
		    input >> input_buf[i];
		}
		// write input buf
		size_t start[] = { t, 0 };
		size_t count[] = { seqLengths[s], inputPattSize };
		if ((ret = nc_put_vara_float(ncid, inputs_varid, start, count, input_buf)) != NC_NOERR)
		{
			cerr << "Could not write inputs: " << nc_strerror(ret) << endl;
			return ret;
		}
		delete[] input_buf;

		//define target buf
		int * target_buf = new int[seqLengths[s]];
		//read target buf
		char * target_buf_char = new char[numLabels * 2 * seqLengths[s]];
		target.read(target_buf_char, numLabels * 2 * seqLengths[s]);
		target.read(tmp, 1);
		for (size_t i = 0; i < seqLengths[s]; i++)
		{
			int idx = 0;
			for (size_t j = i * numLabels * 2; j < (i + 1) * numLabels * 2; j += 2)
			{
				if (target_buf_char[j] == '1')
				{
					target_buf[i] = idx;
					break;
				}
				idx++;
			}
		}
		//write target buf
		size_t start_l[] = { t };
		size_t count_l[] = { seqLengths[s] };
		if ((ret = nc_put_vara_int(ncid, labels_varid, start_l, count_l, target_buf)) != NC_NOERR) 
		{
			cerr << "Could not write target labels: " << nc_strerror(ret) << endl;
			return ret;
		}
		delete[] target_buf;
		delete[] target_buf_char;

		t += seqLengths[s];
	}
	delete[] tmp;
	nc_close(ncid);
	return 0;
}

int main(int argc, char *argv [])
{
	//if (argc < 3)
	//{
	//	cerr << "Usage:" << argv[0] << "read/write" << endl;
	//	cerr << "Examle:" << endl;
	//	cerr << argv[0] << "read filename" << endl;
	//	// write 待加
	//	return 1;
	//}
	////if (argv[1] == "read")
	//if (strncmp(argv[1],"read",4)==0)
	//{
	//	readnc(argv[2]);
	//}

	writenc_prosody(argc, argv);
	//writenc_embedding(argc, argv);
}
